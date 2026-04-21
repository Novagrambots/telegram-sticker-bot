"""Хэндлер приёма медиа и выдачи стикеров.

Флоу:
  Фото             →  выбор (удалить фон / оставить)  →  готовый стикер
  Видео ≤3с        →  сразу обрабатывается             →  готовый стикер
  Видео >3с        →  запрос таймкода  →  сразу обрабатывается

Все temp-файлы чистим в finally.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import tempfile
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    FSInputFile,
    Message,
)

from bot.database import async_session
from bot.database.crud import (
    get_or_create_user,
    get_user_language,
    get_user_packs,
    increment_sticker_count,
    save_last_sticker,
)
from bot.i18n import t
from bot.keyboards.inline import (
    get_back_keyboard,
    get_bg_choice_keyboard,
    get_pack_choose_keyboard,
    get_packs_keyboard,
    get_sticker_done_keyboard,
)
from bot.services.image_processor import process_image
from bot.services.video_processor import get_video_duration, process_video

logger = logging.getLogger(__name__)
router = Router()

TMP_DIR = "/tmp/sticker_bot"
os.makedirs(TMP_DIR, exist_ok=True)

MAX_INPUT_BYTES = 20 * 1024 * 1024

_MEDIA_SEMAPHORE = asyncio.Semaphore(5)


class StickerStates(StatesGroup):
    waiting_bg_choice = State()   # фото — ждём выбор фона
    waiting_timecode = State()    # длинное видео — ждём таймкод


# ==== ВХОД ====

_VIDEO_MIMES = {"video/mp4", "video/webm", "video/quicktime", "video/x-matroska", "image/gif"}


def _is_video_document(message: Message) -> bool:
    if not message.document:
        return False
    mime = (message.document.mime_type or "").lower()
    return mime in _VIDEO_MIMES or mime.startswith("video/")


@router.message(
    F.photo | F.video | F.animation | F.document,
    StateFilter(None, StickerStates.waiting_bg_choice, StickerStates.waiting_timecode),
)
async def handle_media(message: Message, state: FSMContext) -> None:
    async with async_session() as session:
        await get_or_create_user(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
        lang = await get_user_language(session, message.from_user.id)

    is_photo = bool(message.photo) or (
        message.document
        and (message.document.mime_type or "").startswith("image/")
        and not (message.document.mime_type or "").endswith("gif")
    )
    is_video = bool(message.video or message.animation) or _is_video_document(message)

    if not is_photo and not is_video:
        await message.answer(t("error.not_photo_video", lang), parse_mode="HTML")
        return

    if message.photo:
        tg_file = message.photo[-1]
    elif message.video:
        tg_file = message.video
    elif message.animation:
        tg_file = message.animation
    else:
        tg_file = message.document

    file_size = getattr(tg_file, "file_size", None) or 0
    if file_size and file_size > MAX_INPUT_BYTES:
        await message.answer(t("error.file_too_large", lang), parse_mode="HTML")
        return

    # === Фото: показываем выбор фона ===
    if is_photo:
        await state.clear()
        await state.update_data(file_id=tg_file.file_id)
        await state.set_state(StickerStates.waiting_bg_choice)
        await message.answer(
            t("sticker.bg_choice", lang),
            reply_markup=get_bg_choice_keyboard(lang),
            parse_mode="HTML",
        )
        return

    # === Видео: скачиваем, проверяем длительность ===
    await state.clear()
    status_msg = await message.answer(t("sticker.processing", lang), parse_mode="HTML")

    tmp_dir = tempfile.mkdtemp(prefix="vid_", dir=TMP_DIR)
    input_path = os.path.join(tmp_dir, f"{tg_file.file_id}.bin")
    try:
        await message.bot.download(tg_file, destination=input_path)

        try:
            duration = await get_video_duration(input_path)
        except Exception as exc:
            logger.warning("ffprobe упал: %s", exc)
            duration = 0.0

        if duration <= 3.0:
            # короткое видео — сразу обрабатываем
            await _run_video_sticker(
                bot=message.bot,
                user_id=message.from_user.id,
                status_msg=status_msg,
                lang=lang,
                input_path=input_path,
                tmp_dir=tmp_dir,
                start_sec=0.0,
                state=state,
            )
        else:
            # длинное видео — просим таймкод
            await state.update_data(
                input_path=input_path,
                tmp_dir=tmp_dir,
                duration=duration,
            )
            await state.set_state(StickerStates.waiting_timecode)
            await status_msg.edit_text(
                t("sticker.video_too_long", lang, duration=int(duration)),
                parse_mode="HTML",
            )
    except Exception as exc:
        logger.exception("Не удалось принять видео: %s", exc)
        _cleanup_dir(tmp_dir)
        await state.clear()
        await status_msg.edit_text(
            t("error.video_processing", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )


# ==== Таймкод ====

_TC_RE = re.compile(r"^\s*(?:(\d+):)?(\d+(?:\.\d+)?)\s*$")


def _parse_timecode(text: str) -> float | None:
    m = _TC_RE.match(text)
    if not m:
        return None
    minutes = int(m.group(1)) if m.group(1) else 0
    seconds = float(m.group(2))
    return minutes * 60 + seconds


@router.message(StickerStates.waiting_timecode, F.text)
async def handle_timecode(message: Message, state: FSMContext) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)

    start = _parse_timecode(message.text or "")
    if start is None:
        await message.answer(t("sticker.invalid_timecode", lang), parse_mode="HTML")
        return

    data = await state.get_data()
    duration = float(data.get("duration") or 0.0)
    if start < 0 or (duration and start >= duration):
        await message.answer(t("sticker.timecode_out_of_range", lang), parse_mode="HTML")
        return

    input_path = data.get("input_path")
    tmp_dir = data.get("tmp_dir")
    await state.clear()

    status_msg = await message.answer(t("sticker.processing", lang), parse_mode="HTML")
    await _run_video_sticker(
        bot=message.bot,
        user_id=message.from_user.id,
        status_msg=status_msg,
        lang=lang,
        input_path=input_path,
        tmp_dir=tmp_dir,
        start_sec=start,
        state=state,
    )


# ==== Выбор фона: только для фото ====

@router.callback_query(
    F.data.in_({"bg_remove", "bg_keep"}),
    StickerStates.waiting_bg_choice,
)
async def bg_choice(callback: CallbackQuery, state: FSMContext) -> None:
    remove_bg = callback.data == "bg_remove"
    await callback.answer()
    await _process_photo_sticker(callback, state, remove_bg)


# ==== Обработка фото ====

async def _process_photo_sticker(
    callback: CallbackQuery, state: FSMContext, remove_bg: bool
) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)

    data = await state.get_data()
    file_id = data.get("file_id")
    if not file_id:
        await callback.message.edit_text(
            t("error.image_processing", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
        await state.clear()
        return

    try:
        await callback.message.edit_text(
            t("sticker.removing_bg" if remove_bg else "sticker.processing", lang),
            parse_mode="HTML",
        )
    except Exception:
        pass

    async with _MEDIA_SEMAPHORE:
        try:
            buf = await callback.bot.download(file_id)
            image_bytes = buf.read() if hasattr(buf, "read") else bytes(buf)
            webp_bytes = await process_image(image_bytes, remove_bg=remove_bg)
        except Exception as exc:
            logger.exception("Ошибка обработки фото: %s", exc)
            await callback.message.edit_text(
                t("error.image_processing", lang),
                reply_markup=get_back_keyboard(lang),
                parse_mode="HTML",
            )
            await state.clear()
            return

    try:
        sent = await callback.message.answer_sticker(
            BufferedInputFile(webp_bytes, filename="sticker.webp")
        )
        async with async_session() as session:
            await save_last_sticker(session, callback.from_user.id, sent.sticker.file_id, "static")
            await increment_sticker_count(session, callback.from_user.id)
        await callback.message.answer(
            t("sticker.done", lang),
            reply_markup=get_sticker_done_keyboard(lang),
            parse_mode="HTML",
        )
    except Exception as exc:
        logger.exception("Не удалось отправить стикер: %s", exc)
        await callback.message.answer(
            t("error.image_processing", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
    finally:
        await state.clear()


# ==== Обработка видео (без удаления фона) ====

async def _run_video_sticker(
    bot,
    user_id: int,
    status_msg: Message,
    lang: str,
    input_path: str | None,
    tmp_dir: str | None,
    start_sec: float,
    state: FSMContext,
) -> None:
    if not input_path or not os.path.exists(input_path):
        await status_msg.edit_text(
            t("error.video_processing", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
        _cleanup_dir(tmp_dir)
        return

    output_path = os.path.join(tmp_dir, "sticker.webm")

    async with _MEDIA_SEMAPHORE:
        try:
            await process_video(
                input_path=input_path,
                output_path=output_path,
                start_sec=start_sec,
                remove_bg=False,
            )
        except ValueError as exc:
            logger.warning("video too complex: %s", exc)
            await status_msg.edit_text(
                t("error.video_too_complex", lang),
                reply_markup=get_back_keyboard(lang),
                parse_mode="HTML",
            )
            _cleanup_dir(tmp_dir)
            return
        except Exception as exc:
            logger.exception("Ошибка обработки видео: %s", exc)
            await status_msg.edit_text(
                t("error.video_processing", lang),
                reply_markup=get_back_keyboard(lang),
                parse_mode="HTML",
            )
            _cleanup_dir(tmp_dir)
            return

    try:
        sent = await status_msg.answer_sticker(FSInputFile(output_path))
        async with async_session() as session:
            await save_last_sticker(session, user_id, sent.sticker.file_id, "video")
            await increment_sticker_count(session, user_id)
        await status_msg.answer(
            t("sticker.done", lang),
            reply_markup=get_sticker_done_keyboard(lang),
            parse_mode="HTML",
        )
    except Exception as exc:
        logger.exception("Не удалось отправить видеостикер: %s", exc)
        await status_msg.answer(
            t("error.video_processing", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
    finally:
        _cleanup_dir(tmp_dir)


# ==== После отправки стикера ====

@router.callback_query(F.data == "sticker_done")
async def cb_sticker_done(callback: CallbackQuery) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
    try:
        await callback.message.edit_text(t("sticker.thanks", lang), parse_mode="HTML")
    except Exception:
        await callback.message.answer(t("sticker.thanks", lang), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "save_to_pack")
async def cb_save_to_pack(callback: CallbackQuery) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        packs = await get_user_packs(session, callback.from_user.id)

    if not packs:
        await callback.message.edit_text(
            t("pack.my_packs_empty", lang),
            reply_markup=get_packs_keyboard([], lang),
            parse_mode="HTML",
        )
    else:
        await callback.message.edit_text(
            t("pack.choose_pack", lang),
            reply_markup=get_pack_choose_keyboard(packs, lang),
            parse_mode="HTML",
        )
    await callback.answer()


# ==== Утилиты ====

def _cleanup_dir(tmp_dir: str | None) -> None:
    if not tmp_dir:
        return
    try:
        p = Path(tmp_dir)
        if not p.exists():
            return
        for f in p.glob("*"):
            try:
                f.unlink(missing_ok=True)
            except OSError:
                pass
        try:
            p.rmdir()
        except OSError:
            pass
    except Exception as exc:
        logger.debug("cleanup_dir ошибка (не критично): %s", exc)
