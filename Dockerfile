FROM python:3.12-slim

# ffmpeg для конвертации видео в WEBM (анимированные стикеры)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# сначала зависимости (кэшируется Docker слоем)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# предзагрузка модели rembg (u2net) при сборке образа — не при первом запросе
# это позволяет избежать задержки на первый запрос юзера
RUN python -c "from rembg import new_session; new_session('u2net')"

# потом код
COPY bot/ bot/

CMD ["python", "-m", "bot.main"]
