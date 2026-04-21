"""CRUD операции с базой данных"""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Channel, LastStickerBuffer, User, UserStickerPack


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
    full_name: str,
    language: str | None = None,
) -> User:
    """Получить юзера или создать нового"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            language=language or "ru",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def get_user_language(session: AsyncSession, telegram_id: int) -> str:
    """Получить язык юзера (по умолчанию ru)"""
    result = await session.execute(
        select(User.language).where(User.telegram_id == telegram_id)
    )
    lang = result.scalar_one_or_none()
    return lang or "ru"


async def update_user_language(
    session: AsyncSession, telegram_id: int, language: str
) -> None:
    """Обновить язык юзера"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if user:
        user.language = language
        await session.commit()


async def get_active_channels(session: AsyncSession) -> list[Channel]:
    """Получить все каналы для обязательной подписки"""
    result = await session.execute(select(Channel))
    return list(result.scalars().all())


# === Админские функции ===

async def add_channel(
    session: AsyncSession,
    channel_id: int,
    title: str,
    invite_link: str,
) -> Channel:
    """Добавить канал для обязательной подписки"""
    result = await session.execute(
        select(Channel).where(Channel.channel_id == channel_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError(f"Канал {channel_id} уже добавлен")

    channel = Channel(
        channel_id=channel_id,
        title=title,
        invite_link=invite_link,
    )
    session.add(channel)
    await session.commit()
    await session.refresh(channel)
    return channel


async def remove_channel(session: AsyncSession, channel_id: int) -> bool:
    """Удалить канал. Возвращает True если удалён"""
    result = await session.execute(
        select(Channel).where(Channel.channel_id == channel_id)
    )
    channel = result.scalar_one_or_none()
    if not channel:
        return False

    await session.delete(channel)
    await session.commit()
    return True


async def get_user_stats(session: AsyncSession) -> dict:
    """Статистика: всего юзеров, за сегодня, скачиваний"""
    from sqlalchemy import func as sa_func

    total = await session.execute(select(sa_func.count(User.id)))
    total_users = total.scalar() or 0

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_result = await session.execute(
        select(sa_func.count(User.id)).where(User.created_at >= today)
    )
    today_users = today_result.scalar() or 0

    downloads = await session.execute(
        select(sa_func.sum(User.download_count))
    )
    total_downloads = downloads.scalar() or 0

    channels = await session.execute(select(sa_func.count(Channel.id)))
    total_channels = channels.scalar() or 0

    return {
        "total_users": total_users,
        "today_users": today_users,
        "total_downloads": total_downloads,
        "total_channels": total_channels,
    }


async def get_all_user_ids(session: AsyncSession) -> list[int]:
    """Получить все telegram_id юзеров для рассылки"""
    result = await session.execute(select(User.telegram_id))
    return [row[0] for row in result.all()]


# === Буфер последнего стикера (для сохранения в пак) ===

async def save_last_sticker(
    session: AsyncSession,
    telegram_id: int,
    file_id: str,
    sticker_format: str = "static",
) -> LastStickerBuffer:
    """Upsert последнего стикера юзера (один буфер на юзера)"""
    user_result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = user_result.scalar_one_or_none()
    if user is None:
        raise ValueError(f"Пользователь {telegram_id} не найден в БД")

    existing = await session.execute(
        select(LastStickerBuffer).where(LastStickerBuffer.user_id == user.id)
    )
    buf = existing.scalar_one_or_none()

    if buf is None:
        buf = LastStickerBuffer(
            user_id=user.id,
            file_id=file_id,
            sticker_format=sticker_format,
        )
        session.add(buf)
    else:
        buf.file_id = file_id
        buf.sticker_format = sticker_format

    await session.commit()
    await session.refresh(buf)
    return buf


async def get_last_sticker(
    session: AsyncSession, telegram_id: int
) -> LastStickerBuffer | None:
    """Получить последний обработанный стикер юзера (для сохранения в пак)"""
    user_result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = user_result.scalar_one_or_none()
    if user is None:
        return None

    result = await session.execute(
        select(LastStickerBuffer).where(LastStickerBuffer.user_id == user.id)
    )
    return result.scalar_one_or_none()


async def increment_sticker_count(session: AsyncSession, telegram_id: int) -> None:
    """Увеличить счётчик созданных стикеров (поле User.download_count)"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if user:
        user.download_count = (user.download_count or 0) + 1
        await session.commit()


# === Стикер-паки пользователей ===

async def get_user_packs(
    session: AsyncSession, telegram_id: int
) -> list[UserStickerPack]:
    """Список паков пользователя"""
    user_result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = user_result.scalar_one_or_none()
    if user is None:
        return []

    result = await session.execute(
        select(UserStickerPack)
        .where(UserStickerPack.user_id == user.id)
        .order_by(UserStickerPack.created_at.desc())
    )
    return list(result.scalars().all())


async def create_user_pack(
    session: AsyncSession,
    telegram_id: int,
    pack_name: str,
    pack_name_full: str,
    title: str,
    pack_type: str = "static",
) -> UserStickerPack:
    """Создать запись о паке юзера (после успешного createNewStickerSet)"""
    user_result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = user_result.scalar_one_or_none()
    if user is None:
        raise ValueError(f"Пользователь {telegram_id} не найден")

    pack = UserStickerPack(
        user_id=user.id,
        pack_name=pack_name,
        pack_name_full=pack_name_full,
        title=title,
        pack_type=pack_type,
    )
    session.add(pack)
    await session.commit()
    await session.refresh(pack)
    return pack


async def delete_user_pack(
    session: AsyncSession, pack_name_full: str, telegram_id: int
) -> bool:
    """Удалить запись пака (по полному имени). Возвращает True если удалён.
    telegram_id нужен, чтобы чужой юзер не смог удалить пак не свой."""
    user_result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = user_result.scalar_one_or_none()
    if user is None:
        return False

    result = await session.execute(
        select(UserStickerPack).where(
            UserStickerPack.pack_name_full == pack_name_full,
            UserStickerPack.user_id == user.id,
        )
    )
    pack = result.scalar_one_or_none()
    if not pack:
        return False

    await session.delete(pack)
    await session.commit()
    return True


async def get_pack_by_full_name(
    session: AsyncSession, pack_name_full: str
) -> UserStickerPack | None:
    """Получить пак по полному имени (…_by_botusername)"""
    result = await session.execute(
        select(UserStickerPack).where(UserStickerPack.pack_name_full == pack_name_full)
    )
    return result.scalar_one_or_none()


async def get_pack_by_full_name_for_user(
    session: AsyncSession, pack_name_full: str, telegram_id: int
) -> UserStickerPack | None:
    """Получить пак по полному имени ТОЛЬКО если он принадлежит юзеру.
    Защищает от обращения к чужому паку через подмену callback_data."""
    user_result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = user_result.scalar_one_or_none()
    if user is None:
        return None
    result = await session.execute(
        select(UserStickerPack).where(
            UserStickerPack.pack_name_full == pack_name_full,
            UserStickerPack.user_id == user.id,
        )
    )
    return result.scalar_one_or_none()
