"""Сервис обработки видео для анимированных стикеров

Формат видеостикера Telegram:
- WebM VP9, 512x512, ≤ 3 сек, ≤ 256 КБ
- 30 fps, без звука, pixel format yuva420p (с альфа-каналом)

Флоу:
1. ffprobe — длительность (чтобы решить, нужен ли таймкод)
2. ffmpeg:
   - [-ss start -t 3 -i input]
   - scale+pad до 512x512 с прозрачным фоном
   - libvpx-vp9, битрейт авторегулируется 256k → 226k → 196k
3. Опционально rembg покадрово (тяжело! через тот же семафор что и image_processor)
"""
from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from bot.services.image_processor import REMBG_SEMAPHORE, _remove_background_sync

logger = logging.getLogger(__name__)

# лимиты Telegram для видеостикера
MAX_STICKER_BYTES = 256 * 1024
STICKER_SIZE = 512
MAX_DURATION = 3.0

# ступенька снижения битрейта, kbit/s
_BITRATES = ["256k", "226k", "196k"]


# максимальное время одного вызова ffmpeg/ffprobe (сек).
# Видео короткие (≤3 сек выходного материала), 120 сек — более чем достаточно
# и защищает от подвисшего процесса.
_SUBPROCESS_TIMEOUT = 120.0


async def _run(cmd: List[str]) -> tuple[int, bytes, bytes]:
    """Запускает subprocess, возвращает (returncode, stdout, stderr).
    Таймаут защищает от зависших ffmpeg-процессов."""
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=_SUBPROCESS_TIMEOUT
        )
    except asyncio.TimeoutError:
        # подвисший процесс — убиваем принудительно
        try:
            proc.kill()
            await proc.wait()
        except ProcessLookupError:
            pass
        raise RuntimeError(
            f"subprocess timeout ({_SUBPROCESS_TIMEOUT} сек): {cmd[0]}"
        )
    return proc.returncode, stdout, stderr


async def get_video_duration(input_path: str) -> float:
    """Длительность видео в секундах через ffprobe"""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_path,
    ]
    rc, stdout, stderr = await _run(cmd)
    if rc != 0:
        raise RuntimeError(f"ffprobe error: {stderr.decode(errors='replace')}")
    try:
        return float(stdout.decode().strip())
    except ValueError as exc:
        raise RuntimeError(f"ffprobe вернул некорректную длительность: {stdout!r}") from exc


def _scale_pad_filter() -> str:
    """Фильтр ffmpeg: scale с сохранением пропорций + pad до 512x512 + 30fps"""
    return (
        "scale=512:512:force_original_aspect_ratio=decrease,"
        "pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000,"
        "fps=30"
    )


async def _encode_webm(
    input_path: str,
    output_path: str,
    start_sec: float,
    bitrate: str,
) -> None:
    """Один проход ffmpeg: вход → WebM VP9 512x512 ≤3с с указанным битрейтом"""
    cmd = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-ss", str(start_sec),
        "-t", str(MAX_DURATION),
        "-i", input_path,
        "-vf", _scale_pad_filter(),
        "-c:v", "libvpx-vp9",
        "-b:v", bitrate,
        "-an",
        "-auto-alt-ref", "0",
        "-pix_fmt", "yuva420p",
        "-f", "webm",
        output_path,
    ]
    rc, _, stderr = await _run(cmd)
    if rc != 0:
        raise RuntimeError(f"ffmpeg error: {stderr.decode(errors='replace')}")


async def _extract_frames_png(input_path: str, frames_dir: str, start_sec: float) -> None:
    """Извлекает кадры 0..3c как PNG (с альфой) в frames_dir/frame_%05d.png"""
    cmd = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-ss", str(start_sec),
        "-t", str(MAX_DURATION),
        "-i", input_path,
        "-vf", _scale_pad_filter(),
        "-pix_fmt", "rgba",
        os.path.join(frames_dir, "frame_%05d.png"),
    ]
    rc, _, stderr = await _run(cmd)
    if rc != 0:
        raise RuntimeError(f"ffmpeg (frames) error: {stderr.decode(errors='replace')}")


async def _assemble_webm_from_frames(
    frames_dir: str,
    output_path: str,
    bitrate: str,
) -> None:
    """Склеивает PNG-кадры обратно в WebM VP9 с прозрачностью"""
    cmd = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-framerate", "30",
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-c:v", "libvpx-vp9",
        "-b:v", bitrate,
        "-an",
        "-auto-alt-ref", "0",
        "-pix_fmt", "yuva420p",
        "-f", "webm",
        output_path,
    ]
    rc, _, stderr = await _run(cmd)
    if rc != 0:
        raise RuntimeError(f"ffmpeg (assemble) error: {stderr.decode(errors='replace')}")


def _remove_bg_on_file(png_path: str) -> None:
    """Читает PNG, удаляет фон, перезаписывает на диске"""
    from PIL import Image
    with Image.open(png_path) as img:
        img = img.convert("RGBA")
        result = _remove_background_sync(img)
    result.save(png_path, "PNG")


async def _process_frames_with_rembg(frames_dir: str) -> None:
    """Обрабатывает все PNG-кадры через rembg (под семафором, каждый в to_thread)"""
    frame_paths = sorted(Path(frames_dir).glob("frame_*.png"))
    if not frame_paths:
        raise RuntimeError("нет кадров для обработки rembg")

    # Семафор — общий с image_processor, чтобы не перегружать CPU
    async def _worker(p: Path) -> None:
        async with REMBG_SEMAPHORE:
            await asyncio.to_thread(_remove_bg_on_file, str(p))

    # обрабатываем последовательно (поштучно), но каждый кадр — в отдельном потоке.
    # параллелить тут нет смысла — семафор всё равно пускает только 2.
    for p in frame_paths:
        await _worker(p)


async def process_video(
    input_path: str,
    output_path: str,
    start_sec: float = 0.0,
    remove_bg: bool = False,
) -> None:
    """Собирает видеостикер ≤256 КБ из любого видео.

    Параметры:
        input_path — путь к исходнику (mp4/gif/webm/…)
        output_path — куда записать .webm-стикер
        start_sec — начало фрагмента (0 для видео ≤3с)
        remove_bg — прогнать каждый кадр через rembg

    Бросает:
        RuntimeError — если ffmpeg/ffprobe вернули ненулевой код
        ValueError("video too complex") — если после 3 попыток всё ещё > 256 КБ
    """
    if remove_bg:
        # тяжёлый путь: кадры → rembg → сборка обратно
        with TemporaryDirectory(prefix="rembg_frames_", dir="/tmp/sticker_bot") as frames_dir:
            await _extract_frames_png(input_path, frames_dir, start_sec)
            await _process_frames_with_rembg(frames_dir)
            last_error: Exception | None = None
            for bitrate in _BITRATES:
                try:
                    await _assemble_webm_from_frames(frames_dir, output_path, bitrate)
                except Exception as exc:
                    last_error = exc
                    continue
                size = os.path.getsize(output_path)
                if size <= MAX_STICKER_BYTES:
                    return
                logger.info("WebM слишком большой (%d байт) при битрейте %s, пробуем ниже", size, bitrate)
            if last_error is not None:
                raise last_error
            raise ValueError("video too complex")
    else:
        # быстрый путь: прямая перекодировка
        last_error: Exception | None = None
        for bitrate in _BITRATES:
            try:
                await _encode_webm(input_path, output_path, start_sec, bitrate)
            except Exception as exc:
                last_error = exc
                continue
            size = os.path.getsize(output_path)
            if size <= MAX_STICKER_BYTES:
                return
            logger.info("WebM слишком большой (%d байт) при битрейте %s, пробуем ниже", size, bitrate)
        if last_error is not None:
            raise last_error
        raise ValueError("video too complex")
