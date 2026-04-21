# bot_4_sticker — Telegram-бот для создания стикеров

Бот создаёт стикеры из фото и видео/GIF. Поддерживает удаление фона, управление стикер-паками, мультиязычность (ru/uz/en).

## Стек

- Python 3.12 + aiogram 3
- PostgreSQL 16 (SQLAlchemy + asyncpg)
- Pillow + rembg (удаление фона, модель u2net)
- ffmpeg (конвертация видео в WEBM для анимированных стикеров)
- Docker + docker-compose

## Быстрый старт

```bash
cp .env.example .env
# заполнить .env: BOT_TOKEN, BOT_USERNAME, DB_PASSWORD, ADMIN_IDS

docker compose up -d --build
```

## Структура

```
bot/
├── main.py              # entrypoint
├── config.py            # настройки из .env
├── i18n.py              # переводы ru/uz/en
├── emojis.py            # кастомные эмодзи
├── database/            # модели и CRUD
├── handlers/            # start, admin, sticker (TODO), pack (TODO)
├── middlewares/         # subscription, rate_limit
├── keyboards/           # inline, admin
├── services/            # image_processor (TODO), video_processor (TODO)
└── utils/               # commands
```

## Разработка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# скопировать и заполнить .env
cp .env.example .env

# запустить PostgreSQL отдельно и указать DB_HOST=localhost в .env
python -m bot.main
```
