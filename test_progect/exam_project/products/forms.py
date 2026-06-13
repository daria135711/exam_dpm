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