FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx supervisor && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Общие зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Копируем конфиг supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Копируем конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Создаём папки
RUN mkdir -p /app/staticfiles /app/media

# Собираем статику
RUN cd /app/catalog-service && python manage.py collectstatic --noinput

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]