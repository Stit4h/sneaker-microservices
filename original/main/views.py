from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Sneaker, Category, Cart, CartItem
import json
from .models import Order, OrderItem
import requests
from django.conf import settings
from django.template.loader import render_to_string

def blog(request):
    cart_total_items = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_total_items = cart.get_total_items()
    return render(request, 'main/blog.html', {'cart_total_items': cart_total_items})


def shop(request, category_slug=None):
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Sneaker.objects.filter(category=category, in_stock=True)
        current_category = category
    else:
        products = Sneaker.objects.filter(in_stock=True)
        current_category = None

    cart_total_items = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_total_items = cart.get_total_items()

    return render(request, 'main/shop.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'cart_total_items': cart_total_items,
    })


def auth_view(request):

    cart_total_items = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_total_items = cart.get_total_items()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'register':
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Этот никнейм уже занят')
                return redirect('auth')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует')
                return redirect('auth')

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password)
            )
            login(request, user)
            return redirect('shop')


        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            # Ищем пользователя по email
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
            if user:
                login(request, user)
                return redirect('shop')
            else:
                messages.error(request, 'Неверный email или пароль')
    return render(request, 'main/auth.html', {'cart_total_items': cart_total_items})

def logout_view(request):
    logout(request)
    return redirect('blog')



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('sneaker')
    total_price = cart.get_total_price()
    cart_total_items = cart.get_total_items()  # ← переименовал

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_total_items': cart_total_items,  # ← теперь одинаково с base.html
    })


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sneaker_id = data.get('sneaker_id')
            quantity = int(data.get('quantity', 1))

            sneaker = Sneaker.objects.get(id=sneaker_id, in_stock=True)
            cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                sneaker=sneaker,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({
                'status': 'success',
                'message': f'{sneaker.name} добавлен в корзину',
                'cart_total_items': cart.get_total_items(),
                'cart_total_price': str(cart.get_total_price())
            })
        except Sneaker.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Товар не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)


@login_required
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
                'item_total': str(cart_item.sneaker.price * cart_item.quantity) if quantity > 0 else '0',
                'cart_total_price': str(cart.get_total_price()),
                'cart_total_items': cart.get_total_items()
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Товар не найден в корзине'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)


@login_required
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


def filter_products(request):
    category_slug = request.GET.get('category', '')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Sneaker.objects.filter(category=category, in_stock=True)
    else:
        products = Sneaker.objects.filter(in_stock=True)

    html = render_to_string('main/products_partial.html', {'products': products})

    return JsonResponse({
        'status': 'success',
        'html': html
    })

def send_telegram_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            text = f"📬 Новое сообщение с сайта!\n\n👤 Имя: {name}\n📧 Email: {email}\n💬 Сообщение: {message}"

            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': settings.TELEGRAM_CHAT_ID,
                'text': text,
                'parse_mode': 'HTML'
            }

            response = requests.post(url, json=payload)

            if response.status_code == 200:
                return JsonResponse({'status': 'success', 'message': 'Сообщение отправлено!'})
            else:
                return JsonResponse({'status': 'error', 'message': f'Ошибка {response.status_code}'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'})

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.error(request, 'Корзина пуста')
        return redirect('cart')

    if request.method == 'POST':
        # Создаём заказ
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price()
        )

        # Переносим товары из корзины в заказ
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                sneaker=cart_item.sneaker,
                quantity=cart_item.quantity,
                price=cart_item.sneaker.price
            )

        # Очищаем корзину
        cart_items.delete()

        # Отправляем уведомление в Telegram
        send_order_notification(order)

        messages.success(request, f'Заказ #{order.id} успешно оформлен!')
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
    })


def send_order_notification(order):
    """Отправка уведомления о заказе в Telegram"""
    try:
        # Формируем список товаров
        items_text = ""
        for item in order.items.all():
            items_text += f"\n• {item.sneaker.name} x{item.quantity} = {item.get_total_price()} ₽"

        text = f"""🛍️ **НОВЫЙ ЗАКАЗ!**

📋 **Заказ #{order.id}**
👤 **Пользователь:** {order.user.username}
📧 **Email:** {order.user.email}
📅 **Дата:** {order.created_at.strftime('%d.%m.%Y %H:%M')}

**Товары:**{items_text}

💰 **Итого:** {order.total_price} ₽
📊 **Статус:** Новый
"""

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown'
        }

        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f'Ошибка отправки в Telegram: {e}')


def order_confirmation(request, order_id):
    """Страница подтверждения заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'main/order_confirmation.html', {'order': order})