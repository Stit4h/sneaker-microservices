FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8003

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8003 order_app.wsgi:application"]