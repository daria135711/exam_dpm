# vievs.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Product
from .forms import ProductForm

def health_check(request):
    return JsonResponse({'status': 'ok'})

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
            return redirect('products:index') 
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
            return redirect('products:index') 
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
        return redirect('products:index')
    return render(request, 'products/confirm_delete.html', {'object': product})

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


# создать файл forms в products
from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'sku']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название товара',
            'category': 'Категория',
            'price': 'Цена',
            'sku': 'Артикул',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or name.strip() == '':
            raise ValidationError('Название товара не может быть пустым')
        return name.strip()

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Цена должна быть больше 0')
        return price

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        instance = getattr(self, 'instance', None)
        if Product.objects.filter(sku=sku).exclude(pk=instance.pk if instance else None).exists():
            raise ValidationError('Товар с таким артикулом уже существует')
        return sku

# Шаблоны в 4-е