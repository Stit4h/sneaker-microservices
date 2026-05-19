FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код сервиса
COPY . .

# Создаём папки
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8001

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8001 auth_app.wsgi:application"]