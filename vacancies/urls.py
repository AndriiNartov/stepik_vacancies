from django.urls import path

from .views import AllVacanciesView, CompanyDetail, IndexView, VacanciesBySpecialtyView, VacancyDetail


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('vacancies', AllVacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<slug:specialty>', VacanciesBySpecialtyView.as_view(), name='vacancies_by_specialty'),
    path('companies/<int:pk>', CompanyDetail.as_view(), name='companies'),
    path('vacancies/<int:pk>', VacancyDetail.as_view(), name='vacancy'),

]
