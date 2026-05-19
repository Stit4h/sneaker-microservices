from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Sneaker, Category


def blog(request):
    return render(request, 'main/blog.html')


def shop(request, category_slug=None):
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Sneaker.objects.filter(category=category, in_stock=True)
        current_category = category
    else:
        products = Sneaker.objects.filter(in_stock=True)
        current_category = None

    return render(request, 'main/shop.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    })


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