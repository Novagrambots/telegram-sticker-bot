"""Модели базы данных — User, Channel + доменные модели стикеров"""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass


class User(Base):
    """Пользователь бота"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    # когда первый раз зашел в бота
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # сколько стикеров создал
    download_count: Mapped[int] = mapped_column(default=0)
    # язык интерфейса: ru / uz / en
    language: Mapped[str] = mapped_column(String(5), default="ru")

    def __repr__(self) -> str:
        return f"<User {self.telegram_id} ({self.username})>"


class Channel(Base):
    """Канал/группа для обязательной подписки"""
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # id канала в Telegram (например -1001234567890)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    # название для отображения юзеру
    title: Mapped[str] = mapped_column(String(255))
    # ссылка на канал (для кнопки "Подписаться")
    invite_link: Mapped[str] = mapped_column(String(255))
    # когда добавлен
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Channel {self.channel_id} ({self.title})>"


# TODO: добавить доменные модели


class UserStickerPack(Base):
    """Стикер-пак пользователя в Telegram"""
    __tablename__ = "user_sticker_packs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # владелец пака
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    # короткое имя пака (pack_name в Bot API, без суффикса _by_botname)
    # например: "mystickerpack_123"
    pack_name: Mapped[str] = mapped_column(String(64))
    # полное имя пака (pack_name + "_by_" + bot_username)
    # например: "mystickerpack_123_by_mybot"
    pack_name_full: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    # заголовок пака (отображается в Telegram)
    title: Mapped[str] = mapped_column(String(128))
    # тип пака: "static" | "animated" | "video"
    pack_type: Mapped[str] = mapped_column(String(20), default="static")
    # когда создан
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<UserStickerPack {self.pack_name_full} ({self.pack_type})>"


class LastStickerBuffer(Base):
    """Буфер последнего обработанного стикера (для повторной отправки без переобработки)"""
    __tablename__ = "last_sticker_buffer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # один буфер на юзера
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    # file_id Telegram (для повторной отправки без скачивания)
    file_id: Mapped[str] = mapped_column(String(255))
    # формат стикера: "static" | "animated" | "video"
    sticker_format: Mapped[str] = mapped_column(String(20), default="static")
    # когда обновлён
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<LastStickerBuffer user_id={self.user_id} format={self.sticker_format}>"
