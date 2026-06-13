from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date

class Posts(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='заголовок поста',
        help_text='Не может быть пустым'
    )
    content = models.TextField(
        verbose_name='содержание поста',
        help_text='Не может быть пустым'
    )
    published_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    vievs = models.IntegerField(
        default = 0,
        validators=[MinValueValidator(0.01, message='Цена должна быть больше 0')],
        verbose_name='количесиво просмотров'
    )
    is_published = models.BooleanField(
        default = False,
        verbose_name='Статус',
        help_text='Опубликован/черновик'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def clean(self):
        """Валидация на уровне модели"""
        if not self.title or self.title.strip() == '':
            raise ValidationError({'title': 'Заголовок поста не может быть пустым'})
        if not self.content or self.content.strip() == '':
            raise ValidationError({'content': 'Содержание поста не может быть пустым'})
        if self.vievs < 0:
            raise ValidationError({'vievs': 'Просмотры должны быть не меньше 0'})


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Сооб. {self.content})"