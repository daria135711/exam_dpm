# модель в models.py
from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    category = models.CharField(max_length=100, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name="Цена")
    sku = models.CharField(max_length=50, unique=True,
                          verbose_name="Артикул")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    def clean(self):
        """
        Кастомная валидация для модели.
        Вызывается автоматически при сохранении через форму (в том числе в админке).
        """
        # Проверка, что название не пустое
        if not self.name or self.name.strip() == '':
            raise ValidationError({'name': 'Название товара не может быть пустым.'})

        # Проверка, что цена больше нуля
        if self.price <= 0:
            raise ValidationError({'price': 'Цена должна быть больше нуля.'})

        # Проверка уникальности sku (хотя unique=True делает это на уровне БД,
        # но здесь мы можем сделать более красивую ошибку)
        if Product.objects.filter(sku=self.sku).exclude(pk=self.pk).exists():
            raise ValidationError({'sku': 'Товар с таким артикулом уже существует.'})

    def save(self, *args, **kwargs):
        # Вызываем валидацию перед сохранением
        self.full_clean()
        super().save(*args, **kwargs)

# products/admin.py регистрация
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'sku', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'sku')