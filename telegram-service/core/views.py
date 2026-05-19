from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import ContactMessage
import json
import requests


@csrf_exempt
def send_telegram_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            text = f"📬 Новое сообщение с сайта!\n\n👤 Имя: {name}\n📧 Email: {email}\n💬 Сообщение: {message}"

            send_to_telegram(text)

            return JsonResponse({'status': 'success', 'message': 'Сообщение отправлено!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'})


@csrf_exempt
def send_notification(request):
    """Эндпоинт для отправки уведомлений из других сервисов"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')

            send_to_telegram(text)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'})


def send_to_telegram(text):
    """Отправка сообщения в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'HTML'
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f'Ошибка отправки в Telegram: {e}')