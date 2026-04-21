"""Точка входа — запуск стикер-бота"""
import asyncio
import logging
import os
import sys
import time

# uvloop ускоряет asyncio в 2-4 раза (не работает на Windows!)
try:
    import uvloop
    uvloop.install()
except ImportError:
    pass  # на Windows — работаем без uvloop

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings

# настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# флаг-файл для crash recovery
CRASH_FLAG = ".crash_flag"


async def main() -> None:
    """Инициализация и запуск бота"""
    # используем стандартный Bot API (стикеры не превышают 50 МБ)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # подключаем хэндлеры (порядок важен!)
    from bot.handlers import start, admin
    from bot.handlers.sticker import router as sticker_router
    from bot.handlers.pack import router as pack_router

    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(pack_router)
    dp.include_router(sticker_router)  # последний — ловит медиа-сообщения

    # подключаем мидлвари
    from bot.middlewares.rate_limit import RateLimitMiddleware
    from bot.middlewares.subscription import SubscriptionMiddleware

    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())

    @dp.errors()
    async def errors_handler(event, exception: Exception) -> bool:
        if isinstance(exception, TelegramBadRequest):
            msg = str(exception).lower()
            if "query is too old" in msg or "query id is invalid" in msg:
                return True  # просроченный callback — подавляем
        logger.exception("Необработанная ошибка: %s", exception)
        return False

    # события старта и остановки
    async def _background_cleanup() -> None:
        """Фоновая задача: очистка памяти и /tmp каждые 5 минут"""
        import glob
        from bot.middlewares.rate_limit import cleanup_stale_entries
        while True:
            await asyncio.sleep(300)  # 5 минут
            # чистим протухшие записи rate limit (memory leak)
            removed = cleanup_stale_entries()
            if removed:
                logger.info("Фоновая очистка: удалено %d записей rate limit", removed)
            # чистим старые файлы /tmp/sticker_bot (старше 30 минут)
            now = time.time()
            cutoff = now - 30 * 60
            cleaned = 0
            for f in glob.glob("/tmp/sticker_bot/**/*", recursive=True):
                try:
                    if os.path.isfile(f) and os.path.getmtime(f) < cutoff:
                        os.remove(f)
                        cleaned += 1
                except OSError:
                    pass
            if cleaned:
                logger.info("Фоновая очистка: удалено %d временных файлов из /tmp/sticker_bot", cleaned)

    @dp.startup()
    async def on_startup() -> None:
        # создаём таблицы в БД
        from bot.database import engine
        from bot.database.models import Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы БД созданы")

        # проверяем crash recovery
        if os.path.exists(CRASH_FLAG):
            logger.warning("Обнаружен crash-flag — предыдущий запуск завершился аварийно")
            os.remove(CRASH_FLAG)

        # ставим crash-flag (уберём при нормальном завершении)
        with open(CRASH_FLAG, "w") as f:
            f.write("running")

        # запускаем фоновую очистку
        asyncio.create_task(_background_cleanup())
        logger.info("Фоновая очистка запущена (интервал 5 мин)")

        bot_info = await bot.get_me()
        logger.info("Бот @%s запущен!", bot_info.username)

        # ставим дефолтное меню команд (глобально, ru — для новых юзеров)
        from bot.utils.commands import set_default_commands
        await set_default_commands(bot)
        logger.info("Дефолтное меню команд установлено")

    @dp.shutdown()
    async def on_shutdown() -> None:
        # убираем crash-flag при нормальном завершении
        if os.path.exists(CRASH_FLAG):
            os.remove(CRASH_FLAG)
        logger.info("Бот остановлен")

    # запускаем polling
    try:
        logger.info("Запуск polling...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
