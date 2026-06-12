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
