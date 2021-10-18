from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('staff/home', views.staff, name='staff'),
    path('staff/patients', views.patients, name='patients'),
    path('staff/patients/add-patient', views.add_patient, name='add-patient'),
    path('staff/patients/<int:patient_id>', views.patient_vaccinations, name='patient'),
    path('staff/patients/<int:patient_id>/remove', views.remove_patient, name='remove-patient'),
    path('staff/patients/<int:patient_id>/add-dose/<int:vaccination_id>', views.add_dose, name='add-dose'),
    path('staff/patients/<int:patient_id>/add-vaccination', views.add_vaccination, name='add-vaccination'),
    path('staff/patients/<int:patient_id>/history/<int:vaccin_id>', views.vaccination_history, name='vaccination-history'),
    path('private/<int:patient_id>/vaccinations/history/<int:vaccin_id>', views.private_vaccination_history, name='private-vaccination-history'),
    path('staff/vaccins', views.vaccins, name='vaccins'),
    path('private/home', views.private, name='private'),
    path('private/vaccinations', views.vaccinations, name='vaccinations'),
    path('login-staff', views.login_staff, name='login-staff'),
    path('login-private', views.login_private, name='login-private'),
    path('logout-user', views.logout_user, name='logout-user')
]
