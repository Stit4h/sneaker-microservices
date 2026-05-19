from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Cart, CartItem, Order, OrderItem
import json
import requests


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.get_total_price()
    cart_total_items = cart.get_total_items()

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_total_items': cart_total_items,
    })

@csrf_exempt
def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = cart.get_total_items()
    return JsonResponse({'count': count})

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sneaker_id = data.get('sneaker_id')
            sneaker_name = data.get('sneaker_name')
            sneaker_price = data.get('sneaker_price')
            quantity = int(data.get('quantity', 1))

            cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                sneaker_id=sneaker_id,
                defaults={
                    'sneaker_name': sneaker_name,
                    'sneaker_price': sneaker_price,
                    'quantity': quantity
                }
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({
                'status': 'success',
                'message': f'{sneaker_name} добавлен в корзину',
                'cart_total_items': cart.get_total_items(),
                'cart_total_price': str(cart.get_total_price())
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)


@csrf_exempt
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))

            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)

            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()

            cart = request.user.cart
            return JsonResponse({
                'status': 'success',
                'item_total': str(cart_item.sneaker_price * cart_item.quantity) if quantity > 0 else '0',
                'cart_total_price': str(cart.get_total_price()),
                'cart_total_items': cart.get_total_items()
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Товар не найден в корзине'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)


@csrf_exempt
def remove_from_cart(request, item_id):
    if request.method == 'DELETE':
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()

            cart = request.user.cart
            return JsonResponse({
                'status': 'success',
                'cart_total_price': str(cart.get_total_price()),
                'cart_total_items': cart.get_total_items()
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Товар не найден в корзине'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)


@csrf_exempt
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.error(request, 'Корзина пуста')
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price()
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                sneaker_id=cart_item.sneaker_id,
                sneaker_name=cart_item.sneaker_name,
                quantity=cart_item.quantity,
                price=cart_item.sneaker_price
            )

        cart_items.delete()

        send_order_notification(order)

        messages.success(request, f'Заказ #{order.id} успешно оформлен!')
        return redirect(f'/orders/confirmation/{order.id}/')

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
    })


def send_order_notification(order):
    """Отправка уведомления о заказе в Telegram"""
    try:
        items_text = ""
        for item in order.items.all():
            items_text += f"\n• {item.sneaker_name} x{item.quantity} = {item.get_total_price()} ₽"

        text = f"""🛍️ НОВЫЙ ЗАКАЗ!

📋 Заказ #{order.id}
👤 Пользователь: {order.user.username}
📧 Email: {order.user.email}
📅 Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}

Товары:{items_text}

💰 Итого: {order.total_price} ₽
📊 Статус: Новый"""

        # Отправка через telegram-service
        requests.post('http://telegram-service:8004/send-notification/', json={
            'text': text
        }, timeout=5)
    except Exception as e:
        print(f'Ошибка отправки в Telegram: {e}')


def order_confirmation(request, order_id):
    """Страница подтверждения заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'main/order_confirmation.html', {'order': order})