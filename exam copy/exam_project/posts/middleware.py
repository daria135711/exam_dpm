import os
from datetime import datetime
from django.conf import settings

class RequestMetricsMiddleware:
    """Middleware для подсчёта статистики запросов"""

    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.requests_2xx = 0
        self.requests_4xx = 0
        self.requests_5xx = 0
        
        # Определяем путь к файлу логов
        self.log_file = os.path.join(settings.BASE_DIR, 'metrics.log')
        
        # Создаём файл логов, если его нет
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Лог метрик запросов\n")
                f.write(f"# Создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")

    def __call__(self, request):
        # Увеличиваем общее количество запросов
        self.total_requests += 1
        
        # Запоминаем время начала запроса
        start_time = datetime.now()

        # Получаем ответ
        response = self.get_response(request)
        
        # Вычисляем время выполнения запроса
        execution_time = (datetime.now() - start_time).total_seconds()

        # Классифицируем по статусу
        status_code = response.status_code
        if 200 <= status_code < 300:
            self.requests_2xx += 1
        elif 400 <= status_code < 500:
            self.requests_4xx += 1
        elif 500 <= status_code < 600:
            self.requests_5xx += 1

        # Логируем метрики
        self._log_metrics(request, response, execution_time)

        return response

    def _log_metrics(self, request, response, execution_time):
        """Логирование метрик в консоль и файл"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_code = response.status_code
        
        # Формируем сообщение для текущего запроса
        request_log = (
            f"[{timestamp}] "
            f"{request.method} {request.path} "
            f"→ Status: {status_code} "
            f"({execution_time:.3f}s)"
        )
        
        # Формируем статистику
        stats_log = (
            f"[{timestamp}] STATS → "
            f"Total: {self.total_requests} | "
            f"2xx: {self.requests_2xx} | "
            f"4xx: {self.requests_4xx} | "
            f"5xx: {self.requests_5xx}"
        )
        
        # Вывод в консоль
        print(request_log)
        print(stats_log)
        print("-" * 80)
        
        # Запись в файл
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(request_log + '\n')
                f.write(stats_log + '\n')
                f.write('-' * 80 + '\n')
                f.write('\n')
        except Exception as e:
            print(f"Ошибка записи в файл логов: {e}")