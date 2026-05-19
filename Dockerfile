FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx supervisor && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Настройка nginx для Render
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Настройка supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Убираем дефолтный nginx сайт
RUN rm -f /etc/nginx/sites-enabled/default

# Создаём папки и собираем статику
RUN mkdir -p /app/staticfiles /app/media
RUN cd /app/catalog-service && python manage.py collectstatic --noinput

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]