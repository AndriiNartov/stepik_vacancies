import debug_toolbar

from django.conf import settings

from django.contrib import admin

from django.urls import include, path

from vacancies.views import custom_handler404, custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancies.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = custom_handler404

handler500 = custom_handler500
