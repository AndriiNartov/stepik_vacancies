import django
import os
from vacancies.data import companies, jobs, specialties

'''Эти 2 строки кода ниже: создание переменной среды и вызов функции django.setup() необходимы для того, чтобы внутри
нашего приложения Django мы отдельно смогли запустить скрипт, который будет брать данные из файла data.py и на основании
этих данных создавать записи в таблицах БД. Чтобы скрипт корректно запускался, нам необходимо импортировать наши
модели уже после сохранения переменной среды и вызова функции django.setup() (информация из документации Django
https://docs.djangoproject.com/en/3.0/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage).
В связи с этим, при проверки кода, flake8 будет выдавать 1 предупреждение, связанное именно с этим импортом.
В репозитории находится уже заполненный файл базы данных, то есть,  уже после выполнения скрипта.
Чтобы проверить работу скрипта необходимо удалить файл с БД, удалить файл миграций 0001_initial.py, затем
выполнить команды: python manage.py makemigrations и python manage.py migrate. После этого можно запускать данный
скрипт для записи информации в БД из файла data.py'''

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stepik_vacancies.settings")
django.setup()


from vacancies.models import Company, Specialty, Vacancy


for company in companies:
    new_company = Company(
        name=company['title'],
        logo=company['logo'],
        employee_count=company['employee_count'],
        location=company['location'],
        description=company['description']
    )
    new_company.save()

for specialty in specialties:
    new_specialty = Specialty(
        title=specialty['title'],
        code=specialty['code'],
    )
    new_specialty.save()


for job in jobs:
    new_job = Vacancy(
        title=job['title'],
        specialty=Specialty.objects.get(code=job['specialty']),
        company=Company.objects.get(id=int(job['company'])),
        salary_min=job['salary_from'],
        salary_max=job['salary_to'],
        published_at=job['posted'],
        skills=job['skills'],
        description=job['description']
    )
    new_job.save()
