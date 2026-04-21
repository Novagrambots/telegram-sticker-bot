# tg-sticker-bot — Telegram-бот для создания стикеров

Бот создаёт стикеры из фото и видео/GIF. Поддерживает удаление фона, управление стикер-паками, мультиязычность (ru/uz/en).

## Возможности

- 📸 Статичные стикеры из фото (512×512 WebP)
- 🎬 Анимированные стикеры из видео/GIF (512×512 WebM, ≤3 сек)
- ✂️ Удаление фона через rembg (u2net)
- 📦 Создание и управление стикер-паками
- 🌐 Мультиязычность (русский, узбекский, английский)
- 🔒 Обязательная подписка на каналы
- 👮 Админ-панель (статистика, каналы, рассылка)

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
├── handlers/
│   ├── start.py         # /start, меню, профиль, язык, подписка
│   ├── admin.py         # /admin: статистика, каналы, рассылка
│   ├── sticker.py       # приём фото/видео, создание стикеров
│   └── pack.py          # управление стикер-паками (/mypack)
├── services/
│   ├── image_processor.py  # обработка фото (Pillow + rembg)
│   └── video_processor.py  # обработка видео в WEBM (ffmpeg)
├── middlewares/         # subscription, rate_limit
├── keyboards/           # inline, admin
└── utils/               # commands
```

## Команды бота

| Команда     | Описание                    |
|-------------|-----------------------------|
| `/start`    | Запустить бота              |
| `/menu`     | Главное меню                |
| `/mypack`   | Мои стикер-паки             |
| `/profile`  | Мой профиль                 |
| `/language` | Сменить язык                |
| `/help`     | Помощь                      |
| `/cancel`   | Отменить текущее действие   |
| `/admin`    | Админ-панель                |

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
