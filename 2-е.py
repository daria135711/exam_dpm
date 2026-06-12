# В папке вашего приложения (например, products) создайте файл middleware.py
import time

class MetricsMiddleware:
    """
    Middleware для сбора метрик HTTP-запросов.
    Считает общее количество запросов и количество ответов с кодами 2xx,
    4xx, 5xx.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Инициализация счётчиков (атрибуты класса)
        self.total_requests = 0
        self.status_2xx = 0
        self.status_4xx = 0
        self.status_5xx = 0
        self.request_count_since_last_log = 0

    def __call__(self, request):
        # Обработка запроса
        response = self.get_response(request)

        # Увеличиваем общий счётчик
        self.total_requests += 1
        self.request_count_since_last_log += 1

        # Определяем категорию статуса ответа
        status_code = response.status_code
        if 200 <= status_code < 300:
            self.status_2xx += 1
        elif 400 <= status_code < 500:
            self.status_4xx += 1
        elif 500 <= status_code < 600:
            self.status_5xx += 1

        # Выводим статистику каждые 5 запросов (или каждый раз – по желанию)
        if self.request_count_since_last_log >= 5:
            self._log_metrics()
            self.request_count_since_last_log = 0

        return response

    def _log_metrics(self):
        """Выводит накопленную статистику в консоль."""
        print("=== METRICS ===")
        print(f"Total requests: {self.total_requests}")
        print(f"2xx: {self.status_2xx}, 4xx: {self.status_4xx}, 5xx: {self.status_5xx}")
        print("===============")

# В начале файла settings.py добавьте код загрузки переменных
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Читаем настройки из окружения с значениями по умолчанию
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Для учебных целей разрешаем все хосты (в реальном проекте указывайте конкретные)
ALLOWED_HOSTS = ['*']

# Если у вас нет главной страницы (вы используете только админку), создайте 
# простой эндпоинт, возвращающий статус 200. Добавьте в products/views.py

from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})

# В products/urls.py добавьте маршрут:

urlpatterns = [
    path('', views.product_list, name='product_list'),  # если у вас уже есть
    path('ping/', views.health_check, name='ping'),
    # другие маршруты...
]

# В файле products/tests.py напишите:
from django.test import TestCase, Client


class HealthCheckTest(TestCase):
    def test_ping_endpoint(self):
        client = Client()
        response = client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

