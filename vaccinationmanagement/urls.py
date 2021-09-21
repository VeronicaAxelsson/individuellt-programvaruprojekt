from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('staff/home', views.staff, name='staff'),
    path('staff/patients', views.patients, name='patients'),
    path('staff/patients/<int:patient_id>', views.patient_vaccinations, name='patient'),
    path('staff/vaccins', views.vaccins, name='vaccins'),
    path('private/home', views.private, name='private'),
    path('private/vaccinations', views.vaccinations, name='vaccinations')
]
