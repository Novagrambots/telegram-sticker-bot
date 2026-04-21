"""Сервис обработки изображений для создания статичных стикеров

Формат стикера Telegram (статический):
- WebP, 512x512, с прозрачным фоном
- ≤ 512 КБ

Флоу:
1. Open+EXIF-транспозиция (правильная ориентация с телефонов)
2. Опционально удаление фона (rembg, модель u2net, CPU-heavy — через семафор)
3. Ресайз по большей стороне до 512 px (thumbnail, LANCZOS)
4. Центрируем на прозрачном 512x512 канвасе
5. Сохраняем WebP quality=95; если > 512 КБ — снижаем шагом 5 до 50
"""
from __future__ import annotations

import asyncio
import io
import logging
from typing import Optional

from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

# Лимит стикера Telegram
STICKER_SIZE = 512
MAX_STICKER_BYTES = 512 * 1024

# Семафор для тяжёлых операций rembg (CPU-bound).
# 2 параллельных — безопасно для слабых VPS, хватает для десятка юзеров.
# Используется и в video_processor.py при покадровой обработке.
REMBG_SEMAPHORE = asyncio.Semaphore(2)

# Ленивая инициализация rembg-сессии (модель u2net).
# Модель предзагружается в Dockerfile, но инициализация сессии — дело пары секунд.
_rembg_session = None
_rembg_available: Optional[bool] = None


def _get_rembg_session():
    """Lazy init rembg-сессии (один раз на процесс)"""
    global _rembg_session, _rembg_available
    if _rembg_available is False:
        return None
    if _rembg_session is not None:
        return _rembg_session
    try:
        from rembg import new_session
        _rembg_session = new_session("u2net")
        _rembg_available = True
        logger.info("rembg session (u2net) инициализирована")
        return _rembg_session
    except Exception as exc:
        logger.warning("rembg недоступен: %s", exc)
        _rembg_available = False
        return None


def _remove_background_sync(image: Image.Image) -> Image.Image:
    """Синхронное удаление фона через rembg. Вызывается в executor/to_thread."""
    from rembg import remove
    session = _get_rembg_session()
    if session is None:
        return image
    # rembg понимает RGBA → возвращает RGBA с альфа-каналом
    return remove(image, session=session)


def _fit_to_sticker_canvas(image: Image.Image) -> Image.Image:
    """Масштабирует под 512px по большей стороне и центрирует на прозрачном 512x512.
    Telegram требует, чтобы одна из сторон стикера была ровно 512 px — поэтому маленькие
    картинки апскейлим (thumbnail их НЕ увеличивает, только уменьшает)."""
    # RGBA обязательно для прозрачности
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    max_side = max(image.width, image.height)
    if max_side < STICKER_SIZE:
        # апскейл до 512 по большей стороне
        ratio = STICKER_SIZE / max_side
        new_size = (int(image.width * ratio), int(image.height * ratio))
        image = image.resize(new_size, Image.LANCZOS)
    else:
        # thumbnail сохраняет пропорции, ужимает по большей стороне до 512
        image.thumbnail((STICKER_SIZE, STICKER_SIZE), Image.LANCZOS)

    # центрируем на прозрачном канвасе
    canvas = Image.new("RGBA", (STICKER_SIZE, STICKER_SIZE), (0, 0, 0, 0))
    offset_x = (STICKER_SIZE - image.width) // 2
    offset_y = (STICKER_SIZE - image.height) // 2
    canvas.paste(image, (offset_x, offset_y), mask=image if image.mode == "RGBA" else None)
    return canvas


def _save_webp_under_limit(image: Image.Image) -> bytes:
    """Сохраняет WebP, понижая quality с 95 шагом 5 пока не попадём в 512 КБ (или minimum=50)"""
    quality = 95
    while quality >= 50:
        buffer = io.BytesIO()
        image.save(buffer, format="WEBP", quality=quality, method=6)
        data = buffer.getvalue()
        if len(data) <= MAX_STICKER_BYTES:
            return data
        quality -= 5
    # всё равно >512 КБ — вернём последний вариант (Telegram может и принять)
    logger.warning(
        "WebP не влез в %d байт даже с quality=50 (итог=%d)",
        MAX_STICKER_BYTES, len(data),
    )
    return data


def _process_sync(image_bytes: bytes, remove_bg: bool) -> bytes:
    """Синхронная обработка (Pillow + fitting + кодирование)"""
    with Image.open(io.BytesIO(image_bytes)) as img:
        # ориентация по EXIF (иначе фото с iPhone валятся набок)
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGBA")

        if remove_bg:
            try:
                img = _remove_background_sync(img)
            except Exception as exc:
                logger.warning("rembg упал, возвращаем без удаления фона: %s", exc)

        img = _fit_to_sticker_canvas(img)
        return _save_webp_under_limit(img)


async def process_image(image_bytes: bytes, remove_bg: bool = False) -> bytes:
    """Обработать изображение в WebP-стикер 512x512.

    - EXIF-транспозиция
    - опционально удаление фона (под семафором REMBG_SEMAPHORE, в to_thread)
    - ресайз по большей стороне до 512
    - центрирование на прозрачном канвасе
    - сжатие до 512 КБ (quality 95 → 50)

    Возвращает bytes WebP.
    """
    if remove_bg:
        # тяжёлая операция — под семафором
        async with REMBG_SEMAPHORE:
            return await asyncio.to_thread(_process_sync, image_bytes, True)
    else:
        # лёгкая ветка — тоже в отдельном потоке чтобы не блокировать loop на больших фото
        return await asyncio.to_thread(_process_sync, image_bytes, False)
