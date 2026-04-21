"""Inline-клавиатуры — меню, подписка, язык"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import settings
from bot.emojis import E_ID
from bot.i18n import t


def get_start_keyboard(user_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    """Главное меню бота"""
    buttons = [
        [InlineKeyboardButton(
            text=t("btn.create_sticker", lang),
            callback_data="create_sticker",
            style="primary",
            icon_custom_emoji_id=E_ID["camera"],
        )],
        [
            InlineKeyboardButton(
                text=t("btn.my_packs", lang),
                callback_data="my_packs",
                style="success",
                icon_custom_emoji_id=E_ID["folder"],
            ),
            InlineKeyboardButton(
                text=t("btn.profile", lang),
                callback_data="my_profile",
                style="success",
                icon_custom_emoji_id=E_ID["profile"],
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.help", lang),
                callback_data="help",
                style="success",
                icon_custom_emoji_id=E_ID["info"],
            ),
            InlineKeyboardButton(
                text=t("btn.language", lang),
                callback_data="change_language",
                style="success",
                icon_custom_emoji_id=E_ID["gear"],
            ),
        ],
    ]

    # кнопка админки для админов
    if user_id in settings.admin_id_list:
        buttons.append([InlineKeyboardButton(
            text=t("btn.admin_panel", lang),
            callback_data="admin_panel",
            style="danger",
            icon_custom_emoji_id=E_ID["lock"],
        )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка 'Назад' в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.back", lang),
            callback_data="back_to_menu",
            style="success",
            icon_custom_emoji_id=E_ID["back"],
        )],
    ])


def get_subscription_keyboard(
    channels: list[dict], lang: str = "ru"
) -> InlineKeyboardMarkup:
    """Клавиатура подписки на каналы"""
    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton(
            text=f"{ch['title']}",
            url=ch["invite_link"],
            style="primary",
            icon_custom_emoji_id=E_ID["megaphone"],
        )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.check_sub", lang),
        callback_data="check_subscription",
        style="success",
        icon_custom_emoji_id=E_ID["check"],
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_cancel_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Одна кнопка отмены (для FSM-шагов)"""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=t("btn.cancel", lang),
            callback_data="back_to_menu",
            style="danger",
            icon_custom_emoji_id=E_ID["cross"],
        ),
    ]])


def get_bg_choice_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Для фото: [Удалить фон] [Оставить как есть]"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=t("btn.remove_bg", lang),
                callback_data="bg_remove",
                style="primary",
                icon_custom_emoji_id=E_ID["lightning"],
            ),
            InlineKeyboardButton(
                text=t("btn.keep_bg", lang),
                callback_data="bg_keep",
                style="success",
                icon_custom_emoji_id=E_ID["check"],
            ),
        ],
        [InlineKeyboardButton(
            text=t("btn.cancel", lang),
            callback_data="back_to_menu",
            style="danger",
            icon_custom_emoji_id=E_ID["cross"],
        )],
    ])



def get_sticker_done_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """После отправки стикера: [Сохранить в мой пак] [Готово]"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.save_to_pack", lang),
            callback_data="save_to_pack",
            style="primary",
            icon_custom_emoji_id=E_ID["folder"],
        )],
        [InlineKeyboardButton(
            text=t("btn.done", lang),
            callback_data="sticker_done",
            style="success",
            icon_custom_emoji_id=E_ID["check"],
        )],
    ])


def get_packs_keyboard(packs: list, lang: str = "ru") -> InlineKeyboardMarkup:
    """Список паков юзера + кнопка 'Создать пак'. packs — list[UserStickerPack]"""
    buttons = []
    for pack in packs:
        buttons.append([InlineKeyboardButton(
            text=pack.title,
            callback_data=f"pack_select_{pack.pack_name_full}",
            style="success",
            icon_custom_emoji_id=E_ID["folder"],
        )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.create_pack", lang),
        callback_data="pack_create",
        style="primary",
        icon_custom_emoji_id=E_ID["plus"],
    )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.back", lang),
        callback_data="back_to_menu",
        style="success",
        icon_custom_emoji_id=E_ID["back"],
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_pack_choose_keyboard(packs: list, lang: str = "ru") -> InlineKeyboardMarkup:
    """Выбор пака для добавления стикера (callback pack_add_last_<name_full>)"""
    buttons = []
    for pack in packs:
        buttons.append([InlineKeyboardButton(
            text=pack.title,
            callback_data=f"pack_add_last_{pack.pack_name_full}",
            style="primary",
            icon_custom_emoji_id=E_ID["folder"],
        )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.create_pack", lang),
        callback_data="pack_create",
        style="success",
        icon_custom_emoji_id=E_ID["plus"],
    )])
    buttons.append([InlineKeyboardButton(
        text=t("btn.cancel", lang),
        callback_data="back_to_menu",
        style="danger",
        icon_custom_emoji_id=E_ID["cross"],
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_pack_actions_keyboard(pack_name_full: str, lang: str = "ru") -> InlineKeyboardMarkup:
    """Действия над конкретным паком"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.add_sticker", lang),
            callback_data=f"pack_add_last_{pack_name_full}",
            style="primary",
            icon_custom_emoji_id=E_ID["plus"],
        )],
        [InlineKeyboardButton(
            text=t("btn.del_sticker", lang),
            callback_data=f"pack_del_sticker_{pack_name_full}",
            style="success",
            icon_custom_emoji_id=E_ID["trash"],
        )],
        [InlineKeyboardButton(
            text=t("btn.del_pack", lang),
            callback_data=f"pack_del_{pack_name_full}",
            style="danger",
            icon_custom_emoji_id=E_ID["trash"],
        )],
        [InlineKeyboardButton(
            text=t("btn.back", lang),
            callback_data="my_packs",
            style="success",
            icon_custom_emoji_id=E_ID["back"],
        )],
    ])


def get_confirm_delete_pack_keyboard(pack_name_full: str, lang: str = "ru") -> InlineKeyboardMarkup:
    """Подтверждение удаления пака: [Да, удалить] [Отмена]"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.confirm_delete", lang),
            callback_data=f"pack_del_confirm_{pack_name_full}",
            style="danger",
            icon_custom_emoji_id=E_ID["trash"],
        )],
        [InlineKeyboardButton(
            text=t("btn.cancel", lang),
            callback_data=f"pack_select_{pack_name_full}",
            style="success",
            icon_custom_emoji_id=E_ID["back"],
        )],
    ])


def get_skip_emoji_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка 'Пропустить' (для выбора эмодзи)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn.skip_emoji", lang),
            callback_data="pack_skip_emoji",
            style="success",
            icon_custom_emoji_id=E_ID["check"],
        )],
        [InlineKeyboardButton(
            text=t("btn.cancel", lang),
            callback_data="back_to_menu",
            style="danger",
            icon_custom_emoji_id=E_ID["cross"],
        )],
    ])


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Русский",
                callback_data="set_lang_ru",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_ru"],
            ),
            InlineKeyboardButton(
                text="O'zbek",
                callback_data="set_lang_uz",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_uz"],
            ),
            InlineKeyboardButton(
                text="English",
                callback_data="set_lang_en",
                style="primary",
                icon_custom_emoji_id=E_ID["flag_gb"],
            ),
        ],
    ])
