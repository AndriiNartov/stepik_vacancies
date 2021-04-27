from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views.generic import DetailView, ListView

from vacancies.models import Company, Specialty, Vacancy


class IndexView(ListView):
    model = Specialty
    template_name = 'vacancies/index.html'
    context_object_name = 'specialties'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all().prefetch_related('vacancies')
        context['companies'] = Company.objects.all().prefetch_related('vacancies')
        return context


class AllVacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies/all_vacancies.html'

    def get_queryset(self):
        return Vacancy.objects.all().select_related('company').select_related('specialty')


class VacanciesBySpecialtyView(ListView):
    model = Vacancy
    template_name = 'vacancies/specialty_vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(specialty__code=self
                                      .kwargs['specialty'])\
                                      .select_related('specialty')\
                                      .select_related('company')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty_name'] = Specialty.objects.filter(code=self.kwargs['specialty'])[0].title
        return context


class CompanyDetail(DetailView):
    model = Company
    template_name = 'vacancies/company.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(company=self.kwargs['pk']).select_related('specialty')
        return context


class VacancyDetail(DetailView):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Vacancy.objects.filter(pk=self.kwargs['pk']).select_related('company').select_related('specialty')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Здесь ничего нет')


def custom_handler500(request):
    return HttpResponseServerError('На сервере что-то сломалось')
