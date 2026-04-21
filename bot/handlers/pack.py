"""Хэндлер управления стикер-паками.

Команды и колбэки:
- /mypack  и  callback "my_packs"     — список паков
- pack_create                          — FSM создания пака (имя → заголовок → эмодзи)
- pack_select_<name_full>              — действия над паком
- pack_add_last_<name_full>            — добавить последний стикер из буфера в пак
- pack_del_<name_full>                 — запрос подтверждения удаления
- pack_del_confirm_<name_full>         — удалить пак
- pack_del_sticker_<name_full>         — режим удаления стикера из пака
"""
from __future__ import annotations

import logging
import re

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InputSticker,
    Message,
)

from bot.config import settings
from bot.database import async_session
from bot.database.crud import (
    create_user_pack,
    delete_user_pack,
    get_last_sticker,
    get_or_create_user,
    get_pack_by_full_name,
    get_pack_by_full_name_for_user,
    get_user_language,
    get_user_packs,
)
from bot.i18n import t
from bot.keyboards.inline import (
    get_back_keyboard,
    get_cancel_keyboard,
    get_confirm_delete_pack_keyboard,
    get_pack_actions_keyboard,
    get_packs_keyboard,
    get_skip_emoji_keyboard,
)

logger = logging.getLogger(__name__)
router = Router()


# Telegram-лимиты на паки (берём с запасом; при превышении BadRequest и так прилетит)
MAX_STATIC_STICKERS = 120
MAX_VIDEO_STICKERS = 50

# Telegram: имя должно начинаться с буквы, только [a-zA-Z0-9_], итоговое с суффиксом ≤ 64 символа
PACK_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{0,27}$")


class PackStates(StatesGroup):
    """FSM создания пака + удаления стикера"""
    waiting_pack_name = State()
    waiting_pack_title = State()
    waiting_emoji = State()
    waiting_sticker_delete = State()


# ==== СПИСОК ПАКОВ ====

@router.message(Command("mypack"))
async def cmd_mypack(message: Message) -> None:
    """Команда /mypack — список паков"""
    async with async_session() as session:
        await get_or_create_user(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
        lang = await get_user_language(session, message.from_user.id)
        packs = await get_user_packs(session, message.from_user.id)

    if not packs:
        await message.answer(
            t("pack.my_packs_empty", lang),
            reply_markup=get_packs_keyboard([], lang),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            t("pack.my_packs_title", lang),
            reply_markup=get_packs_keyboard(packs, lang),
            parse_mode="HTML",
        )


@router.callback_query(F.data == "my_packs")
async def cb_my_packs(callback: CallbackQuery, state: FSMContext) -> None:
    """Callback версия: показать список паков"""
    await state.clear()
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        packs = await get_user_packs(session, callback.from_user.id)

    text_key = "pack.my_packs_title" if packs else "pack.my_packs_empty"
    try:
        await callback.message.edit_text(
            t(text_key, lang),
            reply_markup=get_packs_keyboard(packs, lang),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        await callback.message.answer(
            t(text_key, lang),
            reply_markup=get_packs_keyboard(packs, lang),
            parse_mode="HTML",
        )
    await callback.answer()


# ==== ДЕЙСТВИЯ НАД ПАКОМ ====

@router.callback_query(F.data.startswith("pack_select_"))
async def cb_pack_select(callback: CallbackQuery) -> None:
    """Открыть меню действий над паком"""
    pack_name_full = callback.data.removeprefix("pack_select_")

    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        pack = await get_pack_by_full_name(session, pack_name_full)

    if pack is None:
        await callback.answer(t("pack.not_found", lang), show_alert=True)
        return

    try:
        await callback.message.edit_text(
            t("pack.actions_title", lang, title=pack.title, pack_name_full=pack_name_full),
            reply_markup=get_pack_actions_keyboard(pack_name_full, lang),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


# ==== СОЗДАНИЕ ПАКА ====

@router.callback_query(F.data == "pack_create")
async def cb_pack_create(callback: CallbackQuery, state: FSMContext) -> None:
    """Старт FSM создания пака"""
    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)

    # Для создания пака нужен "последний стикер" в буфере.
    # Telegram не умеет создавать пустой пак — первый стикер обязателен.
    async with async_session() as session:
        last = await get_last_sticker(session, callback.from_user.id)
    if last is None:
        await callback.answer()
        await callback.message.edit_text(
            t("pack.no_last_sticker", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
        return

    await state.set_state(PackStates.waiting_pack_name)
    await state.update_data(first_file_id=last.file_id, first_format=last.sticker_format)
    await callback.message.edit_text(
        t("pack.create_name_prompt", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(PackStates.waiting_pack_name, F.text)
async def pack_name_input(message: Message, state: FSMContext) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)

    name = (message.text or "").strip().lower()
    if not PACK_NAME_RE.match(name):
        await message.answer(t("pack.invalid_name", lang), parse_mode="HTML")
        return

    bot_username = (settings.bot_username or (await message.bot.get_me()).username or "").lower()
    pack_name_full = f"{name}_by_{bot_username}"

    # проверяем итоговую длину (Telegram лимит 64 символа)
    if len(pack_name_full) > 64:
        await message.answer(t("pack.invalid_name", lang), parse_mode="HTML")
        return

    pack_name = name

    await state.update_data(
        pack_name=pack_name,
        pack_name_full=pack_name_full,
    )
    await state.set_state(PackStates.waiting_pack_title)
    await message.answer(
        t("pack.create_title_prompt", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(PackStates.waiting_pack_title, F.text)
async def pack_title_input(message: Message, state: FSMContext) -> None:
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)

    title = (message.text or "").strip()
    if not (1 <= len(title) <= 64):
        await message.answer(t("pack.invalid_title", lang), parse_mode="HTML")
        return

    await state.update_data(title=title)
    await state.set_state(PackStates.waiting_emoji)
    await message.answer(
        t("pack.create_emoji_prompt", lang),
        reply_markup=get_skip_emoji_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(PackStates.waiting_emoji, F.text)
async def pack_emoji_input(message: Message, state: FSMContext) -> None:
    """Юзер прислал эмодзи первым символом"""
    text = (message.text or "").strip()
    emoji = text[0] if text else "🤔"
    await _finalize_pack_creation(message, state, emoji)


@router.callback_query(F.data == "pack_skip_emoji", PackStates.waiting_emoji)
async def cb_skip_emoji(callback: CallbackQuery, state: FSMContext) -> None:
    """Пропустить выбор эмодзи — поставим 🤔"""
    await callback.answer()
    await _finalize_pack_creation(callback.message, state, "🤔", user_id=callback.from_user.id)


async def _finalize_pack_creation(
    message: Message,
    state: FSMContext,
    emoji: str,
    user_id: int | None = None,
) -> None:
    """Создать пак в Telegram через Bot API + запись в БД"""
    uid = user_id or message.from_user.id
    async with async_session() as session:
        lang = await get_user_language(session, uid)

    data = await state.get_data()
    pack_name = data.get("pack_name")
    pack_name_full = data.get("pack_name_full")
    title = data.get("title")
    first_file_id = data.get("first_file_id")
    first_format = data.get("first_format") or "static"

    if not (pack_name and pack_name_full and title and first_file_id):
        await state.clear()
        await message.answer(t("pack.not_found", lang), parse_mode="HTML")
        return

    sticker_format = "video" if first_format == "video" else "static"
    sticker = InputSticker(
        sticker=first_file_id,
        emoji_list=[emoji],
        format=sticker_format,
    )

    bot: Bot = message.bot
    logger.info("create_new_sticker_set: name=%r title=%r user_id=%s", pack_name_full, title, uid)
    try:
        await bot.create_new_sticker_set(
            user_id=uid,
            name=pack_name_full,
            title=title,
            stickers=[sticker],
        )
    except TelegramBadRequest as exc:
        err = str(exc).lower()
        if "sticker set name is already occupied" in err or "name is already occupied" in err:
            # возвращаем юзера на шаг ввода имени
            await state.set_state(PackStates.waiting_pack_name)
            await message.answer(
                t("pack.name_taken", lang),
                reply_markup=get_cancel_keyboard(lang),
                parse_mode="HTML",
            )
            return
        logger.exception("Не удалось создать пак: %s", exc)
        await state.clear()
        await message.answer(
            t("error.generic", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
        return

    # Сохраняем в БД
    async with async_session() as session:
        await create_user_pack(
            session=session,
            telegram_id=uid,
            pack_name=pack_name,
            pack_name_full=pack_name_full,
            title=title,
            pack_type=sticker_format,
        )

    await state.clear()
    await message.answer(
        t("pack.created", lang, pack_name_full=pack_name_full, title=title),
        reply_markup=get_back_keyboard(lang),
        parse_mode="HTML",
        disable_web_page_preview=False,
    )


# ==== ДОБАВЛЕНИЕ СТИКЕРА В ПАК ====

@router.callback_query(F.data.startswith("pack_add_last_"))
async def cb_pack_add_last(callback: CallbackQuery) -> None:
    """Добавить последний стикер из буфера в указанный пак"""
    pack_name_full = callback.data.removeprefix("pack_add_last_")

    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        pack = await get_pack_by_full_name(session, pack_name_full)
        last = await get_last_sticker(session, callback.from_user.id)

    if pack is None:
        await callback.answer(t("pack.not_found", lang), show_alert=True)
        return
    if last is None:
        await callback.answer(t("pack.no_last_sticker", lang), show_alert=True)
        return

    sticker_format = "video" if last.sticker_format == "video" else "static"
    sticker = InputSticker(
        sticker=last.file_id,
        emoji_list=["🤔"],
        format=sticker_format,
    )

    try:
        await callback.bot.add_sticker_to_set(
            user_id=callback.from_user.id,
            name=pack_name_full,
            sticker=sticker,
        )
    except TelegramBadRequest as exc:
        err = str(exc).upper()
        if "STICKERSET_INVALID" in err:
            # пак удалён со стороны Telegram — чистим нашу запись
            async with async_session() as session:
                await delete_user_pack(session, pack_name_full, callback.from_user.id)
            await callback.answer(t("pack.not_found", lang), show_alert=True)
            return
        if "STICKERS_TOO_MUCH" in err or "TOO_MUCH" in err:
            await callback.answer(t("pack.full", lang), show_alert=True)
            return
        logger.exception("add_sticker_to_set ошибка: %s", exc)
        await callback.answer(t("error.generic", lang), show_alert=True)
        return

    await callback.answer(t("pack.sticker_added", lang, title=pack.title), show_alert=True)


# ==== УДАЛЕНИЕ ПАКА ====

@router.callback_query(F.data.startswith("pack_del_confirm_"))
async def cb_pack_del_confirm(callback: CallbackQuery) -> None:
    """Подтверждено: удаляем пак"""
    pack_name_full = callback.data.removeprefix("pack_del_confirm_")

    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        # проверка владельца — чужой пак не удалим
        pack = await get_pack_by_full_name_for_user(
            session, pack_name_full, callback.from_user.id
        )
    if pack is None:
        await callback.answer(t("pack.not_found", lang), show_alert=True)
        return

    try:
        await callback.bot.delete_sticker_set(name=pack_name_full)
    except TelegramBadRequest as exc:
        logger.warning("delete_sticker_set ошибка: %s", exc)
        # продолжаем — как минимум удалим из БД

    async with async_session() as session:
        await delete_user_pack(session, pack_name_full, callback.from_user.id)

    await callback.message.edit_text(
        t("pack.deleted", lang),
        reply_markup=get_back_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pack_del_sticker_"))
async def cb_pack_del_sticker(callback: CallbackQuery, state: FSMContext) -> None:
    """Включаем режим ожидания стикера для удаления"""
    pack_name_full = callback.data.removeprefix("pack_del_sticker_")

    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        # проверка владельца — чужой пак трогать нельзя
        pack = await get_pack_by_full_name_for_user(
            session, pack_name_full, callback.from_user.id
        )

    if pack is None:
        await callback.answer(t("pack.not_found", lang), show_alert=True)
        return

    await state.set_state(PackStates.waiting_sticker_delete)
    await state.update_data(pack_name_full=pack_name_full)
    await callback.message.edit_text(
        t("pack.send_sticker_to_delete", lang),
        reply_markup=get_cancel_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pack_del_"))
async def cb_pack_del(callback: CallbackQuery) -> None:
    """Показать подтверждение удаления пака.
    Этот хэндлер идёт ПОСЛЕ pack_del_confirm_ и pack_del_sticker_ — порядок важен!
    Т.к. они все начинаются с 'pack_del_', а aiogram матчит в порядке объявления.
    """
    pack_name_full = callback.data.removeprefix("pack_del_")

    async with async_session() as session:
        lang = await get_user_language(session, callback.from_user.id)
        # проверка владельца — нельзя показать подтверждение удаления чужого пака
        pack = await get_pack_by_full_name_for_user(
            session, pack_name_full, callback.from_user.id
        )

    if pack is None:
        await callback.answer(t("pack.not_found", lang), show_alert=True)
        return

    try:
        await callback.message.edit_text(
            t("pack.confirm_delete", lang, title=pack.title),
            reply_markup=get_confirm_delete_pack_keyboard(pack_name_full, lang),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


# ==== УДАЛЕНИЕ СТИКЕРА ИЗ ПАКА ====

@router.message(PackStates.waiting_sticker_delete, F.sticker)
async def handle_sticker_for_delete(message: Message, state: FSMContext) -> None:
    """Юзер прислал (переслал) стикер — удаляем его из пака"""
    async with async_session() as session:
        lang = await get_user_language(session, message.from_user.id)

    data = await state.get_data()
    pack_name_full = data.get("pack_name_full")
    await state.clear()

    # проверяем что стикер действительно из нашего пака
    sticker_set_name = getattr(message.sticker, "set_name", None)
    if sticker_set_name != pack_name_full:
        await message.answer(
            t("pack.not_found", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
        return

    try:
        await message.bot.delete_sticker_from_set(sticker=message.sticker.file_id)
    except TelegramBadRequest as exc:
        logger.warning("delete_sticker_from_set ошибка: %s", exc)
        await message.answer(
            t("error.generic", lang),
            reply_markup=get_back_keyboard(lang),
            parse_mode="HTML",
        )
        return

    await message.answer(
        t("pack.sticker_deleted", lang),
        reply_markup=get_back_keyboard(lang),
        parse_mode="HTML",
    )
