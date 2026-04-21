"""Мультиязычность — русский, узбекский, английский
Использование: from bot.i18n import t
  t("start.welcome", lang="en", name="John")
"""

from bot.emojis import E

TRANSLATIONS = {
    # === /start ===
    "start.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет, {{name}}!</b>\n\n"
            f"{E['camera']} Я помогу тебе создавать стикеры из фото и видео.\n\n"
            f"{E['pin']} <b>Как пользоваться:</b>\n"
            "Отправь мне фото или видео — "
            f"и я превращу его в стикер! {E['plane']}\n\n"
            "Выбери действие ниже:"
        ),
        "uz": (
            f"{E['bot']} <b>Salom, {{name}}!</b>\n\n"
            f"{E['camera']} Rasm va videodan stiker yaratishda yordam beraman.\n\n"
            f"{E['pin']} <b>Qanday foydalanish:</b>\n"
            "Menga rasm yoki video yuboring — "
            f"men uni stikerga aylantirib beraman! {E['plane']}\n\n"
            "Quyidagi tugmalardan birini tanlang:"
        ),
        "en": (
            f"{E['bot']} <b>Hello, {{name}}!</b>\n\n"
            f"{E['camera']} I'll help you create stickers from photos and videos.\n\n"
            f"{E['pin']} <b>How to use:</b>\n"
            "Just send me a photo or video — "
            f"and I'll turn it into a sticker! {E['plane']}\n\n"
            "Choose an action below:"
        ),
    },

    # === Кнопки главного меню ===
    "btn.create_sticker": {
        "ru": "Создать стикер",
        "uz": "Stiker yaratish",
        "en": "Create sticker",
    },
    "btn.my_packs": {
        "ru": "Мои паки",
        "uz": "Mening paketlarim",
        "en": "My packs",
    },
    "btn.profile": {
        "ru": "Мой профиль",
        "uz": "Mening profilim",
        "en": "My profile",
    },
    "btn.help": {
        "ru": "Помощь",
        "uz": "Yordam",
        "en": "Help",
    },
    "btn.back": {
        "ru": "Назад",
        "uz": "Orqaga",
        "en": "Back",
    },
    "btn.language": {
        "ru": "Сменить язык",
        "uz": "Tilni o'zgartirish",
        "en": "Change language",
    },

    # === Профиль ===
    "profile.title": {
        "ru": (
            f"{E['profile']} <b>Твой профиль</b>\n\n"
            f"{E['edit']} Имя: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['camera']} Стикеров создано: {{sticker_count}}\n"
        ),
        "uz": (
            f"{E['profile']} <b>Sening profiling</b>\n\n"
            f"{E['edit']} Ism: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['camera']} Yaratilgan stikerlar: {{sticker_count}}\n"
        ),
        "en": (
            f"{E['profile']} <b>Your profile</b>\n\n"
            f"{E['edit']} Name: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['camera']} Stickers created: {{sticker_count}}\n"
        ),
    },

    # === Помощь ===
    "help.text": {
        "ru": (
            f"{E['book']} <b>Помощь</b>\n\n"
            f"{E['star']} Отправь фото — получишь статичный стикер\n"
            f"{E['star']} Отправь видео/GIF — получишь анимированный стикер\n"
            f"{E['star']} Используй /mypack для управления паками\n"
            f"{E['lock']} Стикеры создаются в твоём личном паке\n\n"
            f"{E['plane']} По вопросам: @{{admin_username}}"
        ),
        "uz": (
            f"{E['book']} <b>Yordam</b>\n\n"
            f"{E['star']} Rasm yuboring — statik stiker olasiz\n"
            f"{E['star']} Video/GIF yuboring — animatsiyali stiker olasiz\n"
            f"{E['star']} Paketlarni boshqarish uchun /mypack dan foydalaning\n"
            f"{E['lock']} Stikerlar sizning shaxsiy paketingizda yaratiladi\n\n"
            f"{E['plane']} Savollar uchun: @{{admin_username}}"
        ),
        "en": (
            f"{E['book']} <b>Help</b>\n\n"
            f"{E['star']} Send a photo — get a static sticker\n"
            f"{E['star']} Send a video/GIF — get an animated sticker\n"
            f"{E['star']} Use /mypack to manage your packs\n"
            f"{E['lock']} Stickers are created in your personal pack\n\n"
            f"{E['plane']} Contact: @{{admin_username}}"
        ),
    },

    # === Подписка ===
    "sub.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет!</b>\n\n"
            f"{E['camera']} Этот бот создаёт стикеры из фото и видео "
            "— быстро и бесплатно!\n\n"
            f"{E['lock']} <b>Для начала подпишись на каналы ниже:</b>\n\n"
            f"После подписки нажми «{E['check']} Проверить подписку»"
        ),
        "uz": (
            f"{E['bot']} <b>Salom!</b>\n\n"
            f"{E['camera']} Bu bot rasm va videodan stiker yaratadi "
            "— tez va bepul!\n\n"
            f"{E['lock']} <b>Boshlash uchun quyidagi kanallarga obuna bo'ling:</b>\n\n"
            f"Obuna bo'lgandan keyin «{E['check']} Obunani tekshirish» tugmasini bosing"
        ),
        "en": (
            f"{E['bot']} <b>Hello!</b>\n\n"
            f"{E['camera']} This bot creates stickers from photos and videos "
            "— fast and free!\n\n"
            f"{E['lock']} <b>To start, subscribe to the channels below:</b>\n\n"
            f"After subscribing, tap «{E['check']} Check subscription»"
        ),
    },
    "sub.not_subscribed": {
        "ru": (
            f"{E['cross']} <b>Ты ещё не подписался на все каналы:</b>\n\n"
            f"Подпишись и нажми «{E['check']} Проверить подписку» ещё раз."
        ),
        "uz": (
            f"{E['cross']} <b>Sen hali barcha kanallarga obuna bo'lmading:</b>\n\n"
            f"Obuna bo'l va «{E['check']} Obunani tekshirish» tugmasini qayta bos."
        ),
        "en": (
            f"{E['cross']} <b>You haven't subscribed to all channels yet:</b>\n\n"
            f"Subscribe and tap «{E['check']} Check subscription» again."
        ),
    },
    "sub.success": {
        "ru": (
            f"{E['check']} <b>Отлично, {{name}}!</b>\n\n"
            f"Теперь ты можешь пользоваться ботом! {E['plane']}\n\n"
            "Отправь фото или видео для создания стикера."
        ),
        "uz": (
            f"{E['check']} <b>Ajoyib, {{name}}!</b>\n\n"
            f"Endi botdan foydalanishing mumkin! {E['plane']}\n\n"
            "Stiker yaratish uchun rasm yoki video yubor."
        ),
        "en": (
            f"{E['check']} <b>Great, {{name}}!</b>\n\n"
            f"You can now use the bot! {E['plane']}\n\n"
            "Send a photo or video to create a sticker."
        ),
    },
    "btn.check_sub": {
        "ru": "Проверить подписку",
        "uz": "Obunani tekshirish",
        "en": "Check subscription",
    },
    "sub.check_alert_fail": {
        "ru": f"{E['cross']} Подпишись на все каналы!",
        "uz": f"{E['cross']} Barcha kanallarga obuna bo'l!",
        "en": f"{E['cross']} Subscribe to all channels!",
    },
    "sub.check_alert_ok": {
        "ru": f"{E['check']} Подписка подтверждена!",
        "uz": f"{E['check']} Obuna tasdiqlandi!",
        "en": f"{E['check']} Subscription confirmed!",
    },
    "sub.not_required": {
        "ru": f"{E['check']} Подписка не требуется!",
        "uz": f"{E['check']} Obuna talab qilinmaydi!",
        "en": f"{E['check']} No subscription required!",
    },

    # === Ошибки ===
    "error.rate_limit": {
        "ru": f"{E['clock']} <b>Слишком много запросов!</b>\n\nПодожди {{seconds}} секунд и попробуй снова.",
        "uz": f"{E['clock']} <b>Juda ko'p so'rovlar!</b>\n\n{{seconds}} soniya kuting va qayta urinib ko'ring.",
        "en": f"{E['clock']} <b>Too many requests!</b>\n\nWait {{seconds}} seconds and try again.",
    },
    "error.generic": {
        "ru": f"{E['cross']} <b>Что-то пошло не так</b>\n\nПопробуй позже.",
        "uz": f"{E['cross']} <b>Nimadir noto'g'ri ketdi</b>\n\nKeyinroq urinib ko'ring.",
        "en": f"{E['cross']} <b>Something went wrong</b>\n\nPlease try again later.",
    },
    "error.unsupported_format": {
        "ru": f"{E['warning']} <b>Неподдерживаемый формат</b>\n\nОтправь фото или видео/GIF.",
        "uz": f"{E['warning']} <b>Qo'llab-quvvatlanmaydigan format</b>\n\nRasm yoki video/GIF yuboring.",
        "en": f"{E['warning']} <b>Unsupported format</b>\n\nSend a photo or video/GIF.",
    },

    # === Выбор языка ===
    "lang.choose": {
        "ru": f"{E['gear']} <b>Выберите язык:</b>",
        "uz": f"{E['gear']} <b>Tilni tanlang:</b>",
        "en": f"{E['gear']} <b>Choose language:</b>",
    },
    "lang.changed": {
        "ru": f"{E['check']} Язык изменён на русский",
        "uz": f"{E['check']} Til o'zbek tiliga o'zgartirildi",
        "en": f"{E['check']} Language changed to English",
    },

    # === Админ-панель ===
    "admin.title": {
        "ru": f"{E['gear']} <b>Админ-панель</b>\n\nВыбери действие:",
        "uz": f"{E['gear']} <b>Admin panel</b>\n\nAmalni tanlang:",
        "en": f"{E['gear']} <b>Admin panel</b>\n\nChoose an action:",
    },
    "admin.no_access": {
        "ru": f"{E['lock']} У тебя нет доступа к админке.",
        "uz": f"{E['lock']} Sizda admin panelga kirish huquqi yo'q.",
        "en": f"{E['lock']} You don't have access to admin panel.",
    },
    "admin.stats": {
        "ru": (
            f"{E['chart']} <b>Статистика бота</b>\n\n"
            f"{E['users']} Всего юзеров: <b>{{total_users}}</b>\n"
            f"{E['star']} Новых юзеров сегодня: <b>{{today_users}}</b>\n"
            f"{E['download']} Всего стикеров создано: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Каналов: <b>{{total_channels}}</b>"
        ),
        "uz": (
            f"{E['chart']} <b>Bot statistikasi</b>\n\n"
            f"{E['users']} Jami foydalanuvchilar: <b>{{total_users}}</b>\n"
            f"{E['star']} Bugungi yangi foydalanuvchilar: <b>{{today_users}}</b>\n"
            f"{E['download']} Jami yaratilgan stikerlar: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Kanallar: <b>{{total_channels}}</b>"
        ),
        "en": (
            f"{E['chart']} <b>Bot statistics</b>\n\n"
            f"{E['users']} Total users: <b>{{total_users}}</b>\n"
            f"{E['star']} New users today: <b>{{today_users}}</b>\n"
            f"{E['download']} Total stickers created: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Channels: <b>{{total_channels}}</b>"
        ),
    },
    "admin.channels_empty": {
        "ru": f"{E['megaphone']} <b>Каналы</b>\n\nСписок пуст. Добавь канал кнопкой ниже.",
        "uz": f"{E['megaphone']} <b>Kanallar</b>\n\nRo'yxat bo'sh. Quyidagi tugma orqali kanal qo'shing.",
        "en": f"{E['megaphone']} <b>Channels</b>\n\nList is empty. Add a channel using the button below.",
    },
    "admin.channels_title": {
        "ru": f"{E['megaphone']} <b>Каналы для подписки:</b>\n",
        "uz": f"{E['megaphone']} <b>Obuna kanallari:</b>\n",
        "en": f"{E['megaphone']} <b>Subscription channels:</b>\n",
    },
    "admin.add_channel_id": {
        "ru": (
            f"{E['megaphone']} <b>Добавление канала</b>\n\n"
            "Отправь <b>ID канала</b> (например <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} Узнать ID: добавь бота @getmyid_bot в канал"
        ),
        "uz": (
            f"{E['megaphone']} <b>Kanal qo'shish</b>\n\n"
            "<b>Kanal ID</b> raqamini yuboring (masalan <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} ID bilish: @getmyid_bot ni kanalga qo'shing"
        ),
        "en": (
            f"{E['megaphone']} <b>Add channel</b>\n\n"
            "Send the <b>channel ID</b> (e.g. <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} Get ID: add @getmyid_bot to the channel"
        ),
    },
    "admin.add_channel_title": {
        "ru": f"{E['edit']} Теперь отправь <b>название канала</b>:",
        "uz": f"{E['edit']} Endi <b>kanal nomini</b> yuboring:",
        "en": f"{E['edit']} Now send the <b>channel name</b>:",
    },
    "admin.add_channel_link": {
        "ru": (
            f"{E['link']} Теперь отправь <b>ссылку или юзернейм канала</b>\n\n"
            "Принимаю любой формат:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "uz": (
            f"{E['link']} Endi <b>kanal havolasi yoki username</b> yuboring\n\n"
            "Istalgan formatda:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "en": (
            f"{E['link']} Now send the <b>channel link or username</b>\n\n"
            "Any format accepted:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
    },
    "admin.channel_added": {
        "ru": f"{E['check']} <b>Канал добавлен!</b>",
        "uz": f"{E['check']} <b>Kanal qo'shildi!</b>",
        "en": f"{E['check']} <b>Channel added!</b>",
    },
    "admin.confirm_delete": {
        "ru": f"{E['warning']} <b>Удалить канал?</b>\n\nID: <code>{{channel_id}}</code>\n\nЭто действие нельзя отменить.",
        "uz": f"{E['warning']} <b>Kanalni o'chirishni xohlaysizmi?</b>\n\nID: <code>{{channel_id}}</code>\n\nBu amalni qaytarib bo'lmaydi.",
        "en": f"{E['warning']} <b>Delete channel?</b>\n\nID: <code>{{channel_id}}</code>\n\nThis action cannot be undone.",
    },
    "admin.id_not_number": {
        "ru": f"{E['cross']} ID должен быть числом. Попробуй ещё раз:",
        "uz": f"{E['cross']} ID raqam bo'lishi kerak. Qayta urinib ko'ring:",
        "en": f"{E['cross']} ID must be a number. Try again:",
    },
    "admin.title_too_long": {
        "ru": f"{E['cross']} Название слишком длинное (макс 200 символов)",
        "uz": f"{E['cross']} Nom juda uzun (maks 200 belgi)",
        "en": f"{E['cross']} Name is too long (max 200 characters)",
    },
    "admin.link_invalid": {
        "ru": f"{E['cross']} Не удалось распознать ссылку.\nПопробуй ещё:",
        "uz": f"{E['cross']} Havolani aniqlab bo'lmadi.\nQayta urinib ko'ring:",
        "en": f"{E['cross']} Could not parse the link.\nTry again:",
    },

    # === Кнопки админки ===
    "btn.admin_stats": {"ru": "Статистика", "uz": "Statistika", "en": "Statistics"},
    "btn.admin_channels": {"ru": "Каналы", "uz": "Kanallar", "en": "Channels"},
    "btn.admin_home": {"ru": "Главное меню", "uz": "Bosh menyu", "en": "Main menu"},
    "btn.admin_add": {"ru": "Добавить канал", "uz": "Kanal qo'shish", "en": "Add channel"},
    "btn.admin_back": {"ru": "Назад", "uz": "Orqaga", "en": "Back"},
    "btn.admin_cancel": {"ru": "Отмена", "uz": "Bekor qilish", "en": "Cancel"},
    "btn.admin_confirm_del": {"ru": "Да, удалить", "uz": "Ha, o'chirish", "en": "Yes, delete"},
    "btn.admin_cancel_del": {"ru": "Отмена", "uz": "Bekor qilish", "en": "Cancel"},
    "btn.admin_panel": {"ru": "Админ-панель", "uz": "Admin panel", "en": "Admin panel"},
    "btn.admin_broadcast": {"ru": "Рассылка", "uz": "Xabar yuborish", "en": "Broadcast"},

    # === Рассылка ===
    "admin.broadcast_prompt": {
        "ru": f"{E['plane']} <b>Массовая рассылка</b>\n\nОтправь текст/фото/видео для рассылки.\nПоддерживается HTML.",
        "uz": f"{E['plane']} <b>Ommaviy xabar</b>\n\nYuborish uchun matn/rasm/video yuboring.\nHTML qo'llab-quvvatlanadi.",
        "en": f"{E['plane']} <b>Mass broadcast</b>\n\nSend text/photo/video to broadcast.\nHTML supported.",
    },
    "admin.broadcast_preview": {
        "ru": f"{E['eye']} <b>Предпросмотр</b>\n\nОтправить это сообщение всем юзерам?",
        "uz": f"{E['eye']} <b>Oldindan ko'rish</b>\n\nBu xabarni barcha foydalanuvchilarga yuborishni xohlaysizmi?",
        "en": f"{E['eye']} <b>Preview</b>\n\nSend this message to all users?",
    },
    "admin.broadcast_confirm": {"ru": "Да, отправить", "uz": "Ha, yuborish", "en": "Yes, send"},
    "admin.broadcast_cancel": {"ru": "Отмена", "uz": "Bekor qilish", "en": "Cancel"},
    "admin.broadcast_started": {
        "ru": f"{E['plane']} Рассылка запущена... Ожидай отчёт.",
        "uz": f"{E['plane']} Xabar yuborilmoqda... Hisobotni kuting.",
        "en": f"{E['plane']} Broadcast started... Wait for report.",
    },
    "admin.broadcast_done": {
        "ru": f"{E['chart']} <b>Рассылка завершена!</b>\n\n{E['check']} Доставлено: <b>{{success}}</b>\n{E['cross']} Ошибок: <b>{{failed}}</b>\n{E['users']} Всего: <b>{{total}}</b>",
        "uz": f"{E['chart']} <b>Xabar yuborish tugadi!</b>\n\n{E['check']} Yetkazildi: <b>{{success}}</b>\n{E['cross']} Xatolar: <b>{{failed}}</b>\n{E['users']} Jami: <b>{{total}}</b>",
        "en": f"{E['chart']} <b>Broadcast complete!</b>\n\n{E['check']} Delivered: <b>{{success}}</b>\n{E['cross']} Failed: <b>{{failed}}</b>\n{E['users']} Total: <b>{{total}}</b>",
    },

    # === Описания команд бота (для меню Telegram) ===
    "cmd.start": {
        "ru": "Запустить бота",
        "uz": "Botni boshlash",
        "en": "Start the bot",
    },
    "cmd.menu": {
        "ru": "Главное меню",
        "uz": "Bosh menyu",
        "en": "Main menu",
    },
    "cmd.profile": {
        "ru": "Мой профиль",
        "uz": "Mening profilim",
        "en": "My profile",
    },
    "cmd.help": {
        "ru": "Помощь",
        "uz": "Yordam",
        "en": "Help",
    },
    "cmd.language": {
        "ru": "Сменить язык",
        "uz": "Tilni o'zgartirish",
        "en": "Change language",
    },
    "cmd.cancel": {
        "ru": "Отменить текущее действие",
        "uz": "Joriy amalni bekor qilish",
        "en": "Cancel current action",
    },
    "cmd.mypack": {
        "ru": "Мои стикер-паки",
        "uz": "Mening stiker paketlarim",
        "en": "My sticker packs",
    },

    # === Стикеры: флоу обработки медиа ===
    "sticker.start_prompt": {
        "ru": f"{E['camera']} <b>Создание стикера</b>\n\nОтправь мне фото или видео/GIF — я превращу его в стикер!",
        "uz": f"{E['camera']} <b>Stiker yaratish</b>\n\nMenga rasm yoki video/GIF yuboring — men uni stikerga aylantiraman!",
        "en": f"{E['camera']} <b>Creating a sticker</b>\n\nSend me a photo or video/GIF — I'll turn it into a sticker!",
    },
    "sticker.bg_choice": {
        "ru": f"{E['camera']} <b>Что сделать с фоном?</b>\n\nЕсли нужен прозрачный фон — нажми «Удалить фон».",
        "uz": f"{E['camera']} <b>Fon bilan nima qilamiz?</b>\n\nShaffof fon kerak bo'lsa — «Fonni olib tashlash» tugmasini bosing.",
        "en": f"{E['camera']} <b>What about the background?</b>\n\nTap \"Remove background\" for transparent sticker.",
    },
    "sticker.bg_choice_video": {
        "ru": (
            f"{E['video']} <b>Что сделать с фоном?</b>\n\n"
            f"{E['warning']} Удаление фона на видео занимает ~1-2 минуты — каждый кадр обрабатывается отдельно."
        ),
        "uz": (
            f"{E['video']} <b>Fon bilan nima qilamiz?</b>\n\n"
            f"{E['warning']} Videoda fonni olib tashlash ~1-2 daqiqa — har bir kadr alohida ishlanadi."
        ),
        "en": (
            f"{E['video']} <b>What about the background?</b>\n\n"
            f"{E['warning']} Removing background from video takes ~1-2 minutes — each frame is processed separately."
        ),
    },
    "sticker.processing": {
        "ru": f"{E['clock']} Обрабатываю... Подожди немного",
        "uz": f"{E['clock']} Ishlov berilyapti... Biroz kuting",
        "en": f"{E['clock']} Processing... Please wait",
    },
    "sticker.removing_bg": {
        "ru": f"{E['refresh']} Удаляю фон...",
        "uz": f"{E['refresh']} Fon olib tashlanmoqda...",
        "en": f"{E['refresh']} Removing background...",
    },
    "sticker.removing_bg_video": {
        "ru": f"{E['refresh']} Удаляю фон с видео (~1-2 минуты)...",
        "uz": f"{E['refresh']} Videodan fon olib tashlanmoqda (~1-2 daqiqa)...",
        "en": f"{E['refresh']} Removing video background (~1-2 min)...",
    },
    "sticker.done": {
        "ru": (
            f"{E['check']} <b>Стикер готов!</b>\n\n"
            "Сохрани его в свой пак — или просто отправь друзьям."
        ),
        "uz": (
            f"{E['check']} <b>Stiker tayyor!</b>\n\n"
            "Uni paketingga saqla — yoki do'stlaringga jo'nat."
        ),
        "en": (
            f"{E['check']} <b>Sticker is ready!</b>\n\n"
            "Save it to your pack — or just send to friends."
        ),
    },
    "sticker.thanks": {
        "ru": f"{E['check']} Отлично! Кидай ещё фото или видео — сделаю больше стикеров.",
        "uz": f"{E['check']} Ajoyib! Yana rasm yoki video yuboring — ko'proq stiker yarataman.",
        "en": f"{E['check']} Great! Send more photos/videos — I'll make more stickers.",
    },
    "sticker.video_too_long": {
        "ru": (
            f"{E['clock']} <b>Видео длиннее 3 секунд</b>\n\n"
            f"{E['video']} Длительность: <b>{{duration}} сек</b>\n\n"
            "Стикер должен быть не больше 3 сек. Пришли таймкод — с какой секунды вырезать?\n\n"
            "Примеры: <code>1</code>, <code>0:15</code>, <code>1:30</code>"
        ),
        "uz": (
            f"{E['clock']} <b>Video 3 soniyadan uzun</b>\n\n"
            f"{E['video']} Davomiyligi: <b>{{duration}} son</b>\n\n"
            "Stiker 3 soniyadan oshmasligi kerak. Qaysi soniyadan kesishni xohlaysiz?\n\n"
            "Masalan: <code>1</code>, <code>0:15</code>, <code>1:30</code>"
        ),
        "en": (
            f"{E['clock']} <b>Video is longer than 3 seconds</b>\n\n"
            f"{E['video']} Duration: <b>{{duration}} sec</b>\n\n"
            "Sticker can't be longer than 3 sec. Send a timecode — from what second to cut?\n\n"
            "Examples: <code>1</code>, <code>0:15</code>, <code>1:30</code>"
        ),
    },
    "sticker.invalid_timecode": {
        "ru": f"{E['cross']} Не понял таймкод. Попробуй формат <code>1</code>, <code>0:15</code> или <code>1:30</code>.",
        "uz": f"{E['cross']} Taymkod tushunarsiz. <code>1</code>, <code>0:15</code> yoki <code>1:30</code> formatini sinab ko'ring.",
        "en": f"{E['cross']} Couldn't parse the timecode. Try <code>1</code>, <code>0:15</code> or <code>1:30</code>.",
    },
    "sticker.timecode_out_of_range": {
        "ru": f"{E['cross']} Таймкод больше длины видео. Попробуй ещё раз.",
        "uz": f"{E['cross']} Taymkod video uzunligidan katta. Qayta urinib ko'ring.",
        "en": f"{E['cross']} Timecode is beyond the video length. Try again.",
    },
    "sticker.bg_failed": {
        "ru": f"{E['warning']} Не удалось удалить фон — отправляю стикер как есть.",
        "uz": f"{E['warning']} Fonni olib tashlab bo'lmadi — stikerni borligicha yuboraman.",
        "en": f"{E['warning']} Couldn't remove background — sending the sticker as is.",
    },

    # === Стикер-паки ===
    "pack.my_packs_title": {
        "ru": f"{E['folder']} <b>Мои стикер-паки</b>\n\nВыбери пак или создай новый:",
        "uz": f"{E['folder']} <b>Mening stiker paketlarim</b>\n\nPaketni tanlang yoki yangisini yarat:",
        "en": f"{E['folder']} <b>My sticker packs</b>\n\nChoose a pack or create a new one:",
    },
    "pack.my_packs_empty": {
        "ru": (
            f"{E['folder']} <b>У тебя пока нет паков</b>\n\n"
            "Создай первый — и я буду складывать твои стикеры туда."
        ),
        "uz": (
            f"{E['folder']} <b>Senda hali paket yo'q</b>\n\n"
            "Birinchisini yarat — men stikerlaringni shu yerga qo'shaman."
        ),
        "en": (
            f"{E['folder']} <b>You don't have any packs yet</b>\n\n"
            "Create the first one — I'll save your stickers there."
        ),
    },
    "pack.choose_pack": {
        "ru": f"{E['folder']} <b>В какой пак сохранить стикер?</b>",
        "uz": f"{E['folder']} <b>Stikerni qaysi paketga saqlash kerak?</b>",
        "en": f"{E['folder']} <b>Which pack should I save this sticker to?</b>",
    },
    "pack.create_name_prompt": {
        "ru": (
            f"{E['plus']} <b>Новый пак — шаг 1 из 3</b>\n\n"
            "Придумай короткое <b>имя пака</b> (буквы/цифры/подчёркивания, до 30 символов).\n\n"
            "Например: <code>my_cats</code>"
        ),
        "uz": (
            f"{E['plus']} <b>Yangi paket — 3 dan 1-qadam</b>\n\n"
            "Paketga qisqa <b>nom</b> o'ylab top (harf/raqam/pastki chiziq, 30 belgigacha).\n\n"
            "Masalan: <code>my_cats</code>"
        ),
        "en": (
            f"{E['plus']} <b>New pack — step 1 of 3</b>\n\n"
            "Choose a short <b>pack name</b> (letters/digits/underscores, up to 30 chars).\n\n"
            "Example: <code>my_cats</code>"
        ),
    },
    "pack.create_title_prompt": {
        "ru": (
            f"{E['edit']} <b>Шаг 2 из 3</b>\n\n"
            "Теперь пришли <b>заголовок</b> пака — то, что будут видеть все (до 64 символов)."
        ),
        "uz": (
            f"{E['edit']} <b>3 dan 2-qadam</b>\n\n"
            "Endi paketning <b>sarlavhasini</b> yubor — bu barchaga ko'rinadi (64 belgigacha)."
        ),
        "en": (
            f"{E['edit']} <b>Step 2 of 3</b>\n\n"
            "Now send the pack <b>title</b> — what everyone will see (up to 64 chars)."
        ),
    },
    "pack.create_emoji_prompt": {
        "ru": (
            f"{E['star']} <b>Шаг 3 из 3</b>\n\n"
            "Пришли эмодзи для первого стикера (или нажми «Пропустить» — поставлю 🤔)."
        ),
        "uz": (
            f"{E['star']} <b>3 dan 3-qadam</b>\n\n"
            "Birinchi stiker uchun emoji yubor (yoki «O'tkazib yuborish» tugmasini bos — 🤔 qo'yaman)."
        ),
        "en": (
            f"{E['star']} <b>Step 3 of 3</b>\n\n"
            "Send an emoji for the first sticker (or tap \"Skip\" — I'll use 🤔)."
        ),
    },
    "pack.invalid_name": {
        "ru": f"{E['cross']} Имя должно быть из латинских букв/цифр/подчёркиваний, 1-30 символов. Попробуй ещё:",
        "uz": f"{E['cross']} Nom lotin harflari/raqamlar/pastki chiziqdan iborat, 1-30 belgi bo'lishi kerak. Qayta urinib ko'ring:",
        "en": f"{E['cross']} Name must be latin letters/digits/underscores, 1-30 chars. Try again:",
    },
    "pack.invalid_title": {
        "ru": f"{E['cross']} Заголовок должен быть 1-64 символа. Попробуй ещё:",
        "uz": f"{E['cross']} Sarlavha 1-64 belgi bo'lishi kerak. Qayta urinib ko'ring:",
        "en": f"{E['cross']} Title must be 1-64 chars. Try again:",
    },
    "pack.name_taken": {
        "ru": f"{E['warning']} Это имя уже занято в Telegram. Придумай другое:",
        "uz": f"{E['warning']} Bu nom Telegramda band. Boshqasini tanlang:",
        "en": f"{E['warning']} This name is already taken in Telegram. Pick another:",
    },
    "pack.created": {
        "ru": (
            f"{E['check']} <b>Пак создан!</b>\n\n"
            f"{E['link']} <a href=\"https://t.me/addstickers/{{pack_name_full}}\">{{title}}</a>\n\n"
            "Теперь ты можешь добавлять туда стикеры."
        ),
        "uz": (
            f"{E['check']} <b>Paket yaratildi!</b>\n\n"
            f"{E['link']} <a href=\"https://t.me/addstickers/{{pack_name_full}}\">{{title}}</a>\n\n"
            "Endi unga stiker qo'sha olasan."
        ),
        "en": (
            f"{E['check']} <b>Pack created!</b>\n\n"
            f"{E['link']} <a href=\"https://t.me/addstickers/{{pack_name_full}}\">{{title}}</a>\n\n"
            "Now you can add stickers to it."
        ),
    },
    "pack.not_found": {
        "ru": f"{E['cross']} Пак не найден.",
        "uz": f"{E['cross']} Paket topilmadi.",
        "en": f"{E['cross']} Pack not found.",
    },
    "pack.deleted": {
        "ru": f"{E['check']} Пак удалён.",
        "uz": f"{E['check']} Paket o'chirildi.",
        "en": f"{E['check']} Pack deleted.",
    },
    "pack.confirm_delete": {
        "ru": (
            f"{E['warning']} <b>Удалить пак «{{title}}»?</b>\n\n"
            "Стикеры внутри пропадут у всех, кто его добавил."
        ),
        "uz": (
            f"{E['warning']} <b>«{{title}}» paketini o'chirmoqchimisan?</b>\n\n"
            "Ichidagi stikerlar qo'shgan barchadan yo'qoladi."
        ),
        "en": (
            f"{E['warning']} <b>Delete pack \"{{title}}\"?</b>\n\n"
            "The stickers inside will disappear for everyone who added the pack."
        ),
    },
    "pack.sticker_added": {
        "ru": f"{E['check']} Стикер добавлен в пак <b>{{title}}</b>!",
        "uz": f"{E['check']} Stiker <b>{{title}}</b> paketiga qo'shildi!",
        "en": f"{E['check']} Sticker added to <b>{{title}}</b>!",
    },
    "pack.sticker_deleted": {
        "ru": f"{E['check']} Стикер удалён из пака.",
        "uz": f"{E['check']} Stiker paketdan o'chirildi.",
        "en": f"{E['check']} Sticker removed from the pack.",
    },
    "pack.full": {
        "ru": f"{E['warning']} Пак переполнен (лимит Telegram).",
        "uz": f"{E['warning']} Paket to'lib ketgan (Telegram chegarasi).",
        "en": f"{E['warning']} Pack is full (Telegram limit).",
    },
    "pack.no_last_sticker": {
        "ru": f"{E['warning']} Нет свежего стикера. Сначала пришли фото или видео.",
        "uz": f"{E['warning']} Yangi stiker yo'q. Avval rasm yoki video yubor.",
        "en": f"{E['warning']} No fresh sticker. Send a photo or video first.",
    },
    "pack.send_sticker_to_delete": {
        "ru": f"{E['trash']} Перешли мне <b>стикер из пака</b>, который надо удалить.",
        "uz": f"{E['trash']} O'chirish kerak bo'lgan <b>paketdagi stikerni</b> yubor.",
        "en": f"{E['trash']} Forward me the <b>sticker from the pack</b> you want to delete.",
    },
    "pack.actions_title": {
        "ru": (
            f"{E['folder']} <b>{{title}}</b>\n"
            f"{E['link']} <a href=\"https://t.me/addstickers/{{pack_name_full}}\">Посмотреть пак</a>\n\n"
            "Что сделать с паком?"
        ),
        "uz": (
            f"{E['folder']} <b>{{title}}</b>\n"
            f"{E['link']} <a href=\"https://t.me/addstickers/{{pack_name_full}}\">Paketni ko'rish</a>\n\n"
            "Paket bilan nima qilamiz?"
        ),
        "en": (
            f"{E['folder']} <b>{{title}}</b>\n"
            f"{E['link']} <a href=\"https://t.me/addstickers/{{pack_name_full}}\">View pack</a>\n\n"
            "What to do with the pack?"
        ),
    },

    # === Ошибки медиа-обработки ===
    "error.not_photo_video": {
        "ru": f"{E['warning']} Отправь фото, видео или GIF — остальное я не умею обрабатывать.",
        "uz": f"{E['warning']} Rasm, video yoki GIF yuboring — boshqa formatlarni ishlay olmayman.",
        "en": f"{E['warning']} Send a photo, video or GIF — I can't handle other formats.",
    },
    "error.file_too_large": {
        "ru": f"{E['warning']} Файл больше 20 МБ — Bot API такое не принимает. Попробуй меньше.",
        "uz": f"{E['warning']} Fayl 20 MB dan katta — Bot API bunday fayllarni qabul qilmaydi. Kichikroqini sinab ko'ring.",
        "en": f"{E['warning']} File is larger than 20 MB — Bot API can't handle it. Try a smaller one.",
    },
    "error.video_processing": {
        "ru": f"{E['cross']} Не удалось обработать видео. Попробуй другое или короче.",
        "uz": f"{E['cross']} Videoni ishlab bo'lmadi. Boshqasini yoki qisqaroqini sinab ko'ring.",
        "en": f"{E['cross']} Couldn't process the video. Try a different or shorter one.",
    },
    "error.image_processing": {
        "ru": f"{E['cross']} Не удалось обработать фото. Попробуй другое.",
        "uz": f"{E['cross']} Rasmni ishlab bo'lmadi. Boshqasini sinab ko'ring.",
        "en": f"{E['cross']} Couldn't process the photo. Try a different one.",
    },
    "error.video_too_complex": {
        "ru": f"{E['warning']} Видео слишком сложное — не влезает в 256 КБ даже на минимальном битрейте. Попробуй фрагмент покороче или попроще.",
        "uz": f"{E['warning']} Video juda murakkab — minimal bitreytda ham 256 KB ga sig'maydi. Qisqaroq yoki oddiyroq fragmentni sinab ko'ring.",
        "en": f"{E['warning']} Video is too complex — doesn't fit in 256 KB even at minimum bitrate. Try a shorter or simpler fragment.",
    },

    # === Кнопки стикер-флоу ===
    "btn.remove_bg": {
        "ru": "Удалить фон",
        "uz": "Fonni olib tashlash",
        "en": "Remove background",
    },
    "btn.remove_bg_video": {
        "ru": "Удалить фон (~1-2 мин)",
        "uz": "Fonni olib tashlash (~1-2 daq)",
        "en": "Remove BG (~1-2 min)",
    },
    "btn.keep_bg": {
        "ru": "Оставить как есть",
        "uz": "Borligicha qoldirish",
        "en": "Keep as is",
    },
    "btn.save_to_pack": {
        "ru": "Сохранить в мой пак",
        "uz": "Paketga saqlash",
        "en": "Save to my pack",
    },
    "btn.done": {
        "ru": "Готово",
        "uz": "Tayyor",
        "en": "Done",
    },
    "btn.create_pack": {
        "ru": "Создать пак",
        "uz": "Paket yaratish",
        "en": "Create pack",
    },
    "btn.add_sticker": {
        "ru": "Добавить стикер",
        "uz": "Stiker qo'shish",
        "en": "Add sticker",
    },
    "btn.del_sticker": {
        "ru": "Удалить стикер",
        "uz": "Stikerni o'chirish",
        "en": "Delete sticker",
    },
    "btn.del_pack": {
        "ru": "Удалить пак",
        "uz": "Paketni o'chirish",
        "en": "Delete pack",
    },
    "btn.skip_emoji": {
        "ru": "Пропустить (🤔)",
        "uz": "O'tkazib yuborish (🤔)",
        "en": "Skip (🤔)",
    },
    "btn.confirm_delete": {
        "ru": "Да, удалить",
        "uz": "Ha, o'chirish",
        "en": "Yes, delete",
    },
    "btn.cancel": {
        "ru": "Отмена",
        "uz": "Bekor qilish",
        "en": "Cancel",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить перевод по ключу и языку"""
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang, translations.get("en", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text


def detect_language(language_code: str | None) -> str:
    """Определяет язык по Telegram: ru → русский, uz → узбекский, остальное → английский"""
    if not language_code:
        return "en"
    if language_code.startswith("ru"):
        return "ru"
    if language_code.startswith("uz"):
        return "uz"
    return "en"
