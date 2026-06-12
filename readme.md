mkdir training_exam
cd training_exam
python3 -m venv venv
source venv/bin/activate
pip install django

django-admin startproject exam_project
cd exam_project
python manage.py startapp products

Откройте файл exam_project/settings.py. Найдите список INSTALLED_APPS и
добавьте в него 'products'

1-е:
создать модель с валидацией (code)

python manage.py makemigrations
python manage.py migrate

Откройте файл products/admin.py и зарегистрируйте модель (code)

python manage.py createsuperuser
python manage.py runserver
перейти в админку, проверить валдацию

2-е
В папке вашего приложения (например, products) создайте файл middleware.py (code)

Откройте exam_project/settings.py и добавьте
products.middleware.MetricsMiddleware в список MIDDLEWARE (лучше в конец,
чтобы не конфликтовать с системными middleware):

Запустите сервер и откройте в браузере несколько страниц админ-панели
(список товаров, добавление, редактирование). В консоли, где запущен
сервер, каждые 5 запросов должна появляться статистика.
Если вы хотите видеть статистику после каждого запроса, замените условие
if self.request_count_since_last_log >= 5: на if True: (или просто
вызывайте self._log_metrics() каждый раз).

pip install python-dotenv

В папке, где находится manage.py, создайте файл .env со следующим
содержимым:
env
DEBUG=False
SECRET_KEY=ваш_секретный_ключ_из_админки

В начале файла settings.py добавьте код загрузки переменных (code)

pip install whitenoise

В MIDDLEWARE добавьте whitenoise.middleware.WhiteNoiseMiddleware сразу
после SecurityMiddleware (до всех остальных middleware)

Добавьте настройки для статики (внизу файла):
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

python manage.py collectstatic (появится папка)

Если у вас нет главной страницы (вы используете только админку), создайте
простой эндпоинт, возвращающий статус 200. Добавьте в products/views.py  (code)

В products/urls.py добавьте маршрут: (code)

В файле products/tests.py напишите: (code)

python manage.py test

3-е
4-e