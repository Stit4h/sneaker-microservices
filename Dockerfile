FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Используем catalog-service как основной (порт 80)
WORKDIR /app/catalog-service

RUN python manage.py collectstatic --noinput

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "catalog_app.wsgi:application"]