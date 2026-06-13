from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название товара',
        help_text='Не может быть пустым'
    )
    category = models.CharField(
        max_length=100,
        verbose_name='Категория товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='Цена должна быть больше 0')],
        verbose_name='Цена'
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Артикул',
        help_text='Уникальный артикул'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def clean(self):
        """Валидация на уровне модели"""
        if not self.name or self.name.strip() == '':
            raise ValidationError({'name': 'Название товара не может быть пустым'})
        if self.price <= 0:
            raise ValidationError({'price': 'Цена должна быть больше 0'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Арт. {self.sku})"