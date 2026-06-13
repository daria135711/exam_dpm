from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Posts
from .forms import PostsForm

def health_check(request):
    return JsonResponse({'status': 'ok'})

def index(request):
    """Главная страница"""
    posts = Posts.objects.all()
    return render(request, 'posts/index.html', {'object_list': posts})

def create(request):
    """Создание нового"""
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение успешно создано!')
            return redirect('posts:index') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form[field].label}: {error}')
    else:
        form = PostsForm()
    return render(request, 'posts/form.html', {'form': form, 'object': None})

def update(request, pk):
    """Редактирование"""
    posts = get_object_or_404(Posts, pk=pk)
    if request.method == 'POST':
        form = PostsForm(request.POST, instance=posts)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно обновлено!')
            return redirect('posts:index') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form[field].label}: {error}')
    else:
        form = PostsForm(instance=posts)
    return render(request, 'posts/form.html', {'form': form, 'object': posts})

def delete(request, pk):
    """Удаление товара"""
    posts = get_object_or_404(Posts, pk=pk)
    if request.method == 'POST':
        posts.delete()
        messages.success(request, 'Успешно удалено!')
        return redirect('posts:index')
    return render(request, 'posts/confirm_delete.html', {'object': posts})