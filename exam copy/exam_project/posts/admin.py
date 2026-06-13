from django.contrib import admin
from .models import Posts

@admin.register(Posts)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'published_at', 'vievs', 'is_published', 'created_at']
    search_fields = ['title']
