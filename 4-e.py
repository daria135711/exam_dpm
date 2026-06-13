# создать templates в products и в templates - products
# templates/products/base.html
<!-- products/templates/products/base.html -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Управление товарами{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg bg-dark navbar-dark">
        <div class="container">
            <!-- ИСПРАВЛЕНО: добавлено products: -->
            <a class="navbar-brand" href="{% url 'products:index' %}">📦 Управление товарами</a>
        </div>
    </nav>
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{% if message.tags == 'error' %}danger{% else %}{{ message.tags }}{% endif %} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

# templates/products/index.html

<!-- products/templates/products/index.html -->
{% extends 'products/base.html' %}

{% block title %}Список товаров{% endblock %}

{% block content %}
<h1>📋 Список товаров</h1>
<!-- ИСПРАВЛЕНО: добавлено products: -->
<a href="{% url 'products:create' %}" class="btn btn-primary mb-3">➕ Добавить товар</a>

<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Категория</th>
            <th>Цена</th>
            <th>Артикул</th>
            <th>Действия</th>
        </tr>
    </thead>
    <tbody>
        {% for obj in object_list %}
        <tr>
            <td>{{ obj.id }}</td>
            <td><strong>{{ obj.name }}</strong></td>
            <td>{{ obj.category }}</td>
            <td>{{ obj.price }} ₽</td>
            <td><code>{{ obj.sku }}</code></td>
            <td>
                <!-- ИСПРАВЛЕНО: добавлено products: -->
                <a href="{% url 'products:update' obj.id %}" class="btn btn-sm btn-warning">✏️ Изменить</a>
                <a href="{% url 'products:delete' obj.id %}" class="btn btn-sm btn-danger">🗑️ Удалить</a>
             </td>
         </tr>
        {% empty %}
         <tr>
            <td colspan="6" class="text-center">📭 Нет товаров. Добавьте первый!</td>
         </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}

# templates/products/form.html

{% extends 'products/base.html' %}

{% block title %}{% if object %}Редактирование товара{% else %}Новый товар{% endif %}{% endblock %}

{% block content %}
<h1>{% if object %}✏️ Редактирование товара{% else %}➕ Новый товар{% endif %}</h1>

<form method="post">
    {% csrf_token %}
    
    {% for field in form %}
    <div class="mb-3">
        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
        {{ field }}
        {% if field.help_text %}
            <div class="form-text">{{ field.help_text }}</div>
        {% endif %}
        {% if field.errors %}
            <div class="alert alert-danger mt-1">
                {% for error in field.errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
    </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-success">💾 Сохранить</button>
    <!-- ВАЖНО: здесь products:index -->
    <a href="{% url 'products:index' %}" class="btn btn-secondary">↩️ Отмена</a>
</form>
{% endblock %}

# templates/products/confirm_delete.html

<!-- products/templates/products/confirm_delete.html -->
{% extends 'products/base.html' %}

{% block title %}Удаление товара{% endblock %}

{% block content %}
<div class="card border-danger">
    <div class="card-header bg-danger text-white">
        <h2>⚠️ Подтверждение удаления</h2>
    </div>
    <div class="card-body">
        <p class="fs-5">Вы уверены, что хотите удалить товар <strong>"{{ object }}"</strong>?</p>
        <p class="text-danger">Это действие невозможно отменить.</p>
        
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">✅ Да, удалить</button>
            <!-- ИСПРАВЛЕНО: добавлено products: -->
            <a href="{% url 'products:index' %}" class="btn btn-secondary">❌ Нет, отмена</a>
        </form>
    </div>
</div>
{% endblock %}


