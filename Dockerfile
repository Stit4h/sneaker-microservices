FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаём папки
RUN mkdir -p /app/staticfiles /app/media

# Миграции и статика
RUN cd /app/catalog-service && python manage.py makemigrations core
RUN cd /app/catalog-service && python manage.py migrate
RUN cd /app/catalog-service && python manage.py collectstatic --noinput

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "catalog_app.wsgi:application"]