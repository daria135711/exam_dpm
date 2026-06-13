from django import forms
from django.core.exceptions import ValidationError
from .models import Posts

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content', 'vievs']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'vievs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'title': 'Заголовок сообщения',
            'content': 'Сообщение',
            'vievs': 'Просмотры',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise ValidationError('Заголовок не может быть пустым')
        return title.strip()

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise ValidationError('Сообщение не может быть пустым')
        return content.strip()
