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
