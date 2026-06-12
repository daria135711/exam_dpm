# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Product
from .forms import ProductForm

def index(request):
    """Главная страница со списком товаров"""
    products = Product.objects.all()
    return render(request, 'products/index.html', {'object_list': products})

def create(request):
    """Создание нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно создан!')
            return redirect('index')
        else:
            # Возврат на форму с сообщением об ошибке
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form[field].label}: {error}')
    else:
        form = ProductForm()
    return render(request, 'products/form.html', {'form': form, 'object': None})

def update(request, pk):
    """Редактирование товара"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлён!')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form[field].label}: {error}')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/form.html', {'form': form, 'object': product})

def delete(request, pk):
    """Удаление товара"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар успешно удалён!')
        return redirect('index')
    return render(request, 'products/confirm_delete.html', {'object': product})

def ping(request):
    """Эндпоинт для интеграционного теста"""
    return HttpResponse("pong", status=200)

# urls.py (products/)
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('ping/', views.ping, name='ping'),
]

#  urls.py (products_project/)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]

# Для отдачи статики при DEBUG=False
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Шаблоны в 4-е