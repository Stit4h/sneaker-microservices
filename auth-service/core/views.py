from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.urls import reverse


def auth_view(request):
    # Очищаем старые сообщения из других сервисов
    list(messages.get_messages(request))

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

            next_url = request.GET.get('next', '/catalog/shop/')
            return redirect(next_url)

        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
            if user:
                login(request, user)

                next_url = request.GET.get('next', '/catalog/shop/')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверный email или пароль')

    return render(request, 'main/auth.html')


def logout_view(request):
    logout(request)
    return redirect('/catalog/')