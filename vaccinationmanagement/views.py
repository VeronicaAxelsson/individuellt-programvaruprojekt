"""
Views
"""
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from vaccinationmanagement.functions import (check_for_booster,
    check_if_patient_has_booster,
    alert_if_booster,
    group_vaccinations
)
from vaccinationmanagement.models import Vaccin, Patient, Vaccination

def index(request):
    """
    Index
    """
    if request.user.groups.filter(name="staff").exists():
        return redirect('staff')
    if request.user.groups.filter(name="patient").exists():
        return redirect('private')
    context = {
        'start_page': 'start-page'
    }
    return render(request, 'vaccinationmanagement/index.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def staff(request):
    """
    Startpage for staff
    """
    booster_alert = alert_if_booster(request)
    context = {
        'booster_alert': booster_alert
    }
    return render(request, 'vaccinationmanagement/staff.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def patients(request):
    """
    Shows all patients and enables search among patients
    """
    booster_alert = alert_if_booster(request)
    staffs_patients = User.objects.get(id=request.user.id).patient_set.all()
    if request.method == "POST":
        searched = request.POST['search-patient']
        if len(searched) != 0:
            staffs_patients = User.objects.get(
                id=request.user.id
            ).patient_set.filter(
                Q(first_name__icontains=searched) |
                Q(last_name__icontains=searched) |
                Q(social_security_nr__icontains=searched)
            )

    for patient in staffs_patients:
        vaccinations = Vaccination.objects.filter(
            patient__patient_id=patient.patient_id
        ).select_related('vaccin')
        if check_if_patient_has_booster(vaccinations):
            patient.upcomming_booster = True
    context = {
        'staffs_patients': staffs_patients,
        'booster_alert': booster_alert
    }
    return render(request, 'vaccinationmanagement/patients.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def patient_vaccinations(request, patient_id):
    """
    Shows the patients vaccinations and enables search among vaccines
    """
    booster_alert = alert_if_booster(request)
    patient = Patient.objects.filter(patient_id=patient_id).values()[0]
    vaccinations = Vaccination.objects.filter(
        patient__patient_id=patient_id
    ).select_related('vaccin').order_by('vaccin')
    grouped_vaccinations = check_for_booster(group_vaccinations(vaccinations))
    if request.method == "POST":
        searched = request.POST['search-vaccinations']
        if len(searched) != 0:
            searched_vaccinations = Vaccination.objects.filter(
                patient__patient_id=patient_id,
                vaccin__vaccin_name__icontains=searched
            )
            grouped_vaccinations = check_for_booster(group_vaccinations(searched_vaccinations))

    context = {
        'patient_id' : patient_id,
        'patient' : patient,
        'vaccinations' : grouped_vaccinations,
        'booster_alert': booster_alert
    }
    return render(request, 'vaccinationmanagement/patient.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def vaccination_history(request, patient_id, vaccin_id):
    """
    Vaccination history of staffs patient
    """
    booster_alert = alert_if_booster(request)
    vaccinations = Vaccination.objects.filter(
        patient__patient_id=patient_id,
        vaccin__vaccin_id=vaccin_id
    )
    patient = Patient.objects.get(patient_id=patient_id)
    vaccin = Vaccin.objects.get(vaccin_id=vaccin_id)
    context = {
        'vaccinations': vaccinations,
        'patient': patient,
        'vaccin': vaccin,
        'booster_alert': booster_alert
    }

    return render(request, 'vaccinationmanagement/history.html', context)

@user_passes_test(lambda u: u.groups.filter(name='patient').exists(), login_url='index')
def private_vaccination_history(request, patient_id, vaccin_id):
    """
    Vaccination history of private person
    """
    booster_alert = alert_if_booster(request)
    vaccinations = Vaccination.objects.filter(
        patient__patient_id=patient_id,
        vaccin__vaccin_id=vaccin_id
    )
    patient = Patient.objects.get(patient_id=patient_id)
    vaccin = Vaccin.objects.get(vaccin_id=vaccin_id)
    context = {
        'vaccinations': vaccinations,
        'patient': patient,
        'vaccin': vaccin,
        'booster_alert': booster_alert
    }

    return render(request, 'vaccinationmanagement/private-history.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def add_dose(request, patient_id, vaccination_id):
    """
    Add dose
    """
    booster_alert = alert_if_booster(request)
    context = {
        'patient_id' : patient_id,
        'vaccination_id': vaccination_id,
        'booster_alert': booster_alert
    }
    if request.method == "POST":
        dose_nr = request.POST['dose_nr']
        date_of_vaccination = request.POST['date_of_vaccination']
        date_of_next_vaccination = request.POST['date_of_next_vaccination']
        note = request.POST['note']
        if 'vaccination_done' in request.POST:
            vaccination_done = True
            date_of_next_vaccination = None
        else:
            vaccination_done = False
        vaccination = Vaccination.objects.get(vaccination_id=vaccination_id)
        ins = Vaccination(
            vaccin=vaccination.vaccin,
            dose_nr=dose_nr,
            date_of_vaccination=date_of_vaccination,
            date_of_next_vaccination=date_of_next_vaccination,
            patient=vaccination.patient,
            vaccination_done=vaccination_done,
            note=note
        )
        ins.save()
        return redirect('patient', patient_id=patient_id)

    context['dose_nr'] = Vaccination.objects.get(vaccination_id=vaccination_id).dose_nr
    return render(request, 'vaccinationmanagement/forms/add-dose.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def add_patient(request):
    """
    Add patient to staffs list
    """
    booster_alert = alert_if_booster(request)
    all_patients = Patient.objects.all().values()
    if request.method == "POST":
        patient_id = request.POST['patient']
        Patient.objects.get(
            patient_id=patient_id
        ).belong_to_users.add(User.objects.get(id=request.user.id))
        return redirect('patients')

    exclude_patients = User.objects.get(id=request.user.id).patient_set.all()
    for exclude_patient in exclude_patients:
        all_patients = all_patients.exclude(patient_id=exclude_patient.patient_id)
    context = {
        'patients' : all_patients,
        'booster_alert': booster_alert
    }
    return render(request, 'vaccinationmanagement/forms/add-patient.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def remove_patient(request, patient_id):
    """
    Remove patient from staffs list
    """
    Patient.objects.get(
        patient_id=patient_id
    ).belong_to_users.remove(User.objects.get(id=request.user.id))
    return redirect('patients')

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def add_vaccination(request, patient_id):
    """
    Add vaccinations to patient
    """
    booster_alert = alert_if_booster(request)
    context = {
        'patient_id' : patient_id
    }
    if request.method == "POST":
        vaccin = Vaccin.objects.get(vaccin_id=request.POST['vaccin'])
        dose_nr = request.POST['dose_nr']
        date_of_vaccination = request.POST['date_of_vaccination']
        date_of_next_vaccination = request.POST['date_of_next_vaccination']
        note = request.POST['note']
        patient = Patient.objects.get(patient_id=request.POST['patient'])
        if 'vaccination_done' in request.POST:
            vaccination_done = True
            date_of_next_vaccination = None
        else:
            vaccination_done = False
        ins = Vaccination(
            vaccin=vaccin,
            dose_nr=dose_nr,
            date_of_vaccination=date_of_vaccination,
            date_of_next_vaccination=date_of_next_vaccination,
            patient=patient,
            vaccination_done=vaccination_done,
            note=note
        )
        ins.save()
        return redirect('patient', patient_id=patient_id)

    all_vaccins = Vaccin.objects.all()
    vaccinations = Vaccination.objects.filter(
        patient__patient_id=patient_id
    ).select_related('vaccin').order_by('vaccin')
    for exclude_vaccin in vaccinations:
        all_vaccins = all_vaccins.exclude(vaccin_id=exclude_vaccin.vaccin_id)
    context = {
        'patient_id' : patient_id,
        'vaccins': all_vaccins,
        'booster_alert': booster_alert
    }
    return render(request, 'vaccinationmanagement/forms/add-vaccination.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def vaccins(request):
    """
    Shows all vaccines and enables search among vaccines
    """
    booster_alert = alert_if_booster(request)
    all_vaccins = Vaccin.objects.all().values()
    if request.method == "POST":
        searched = request.POST['search-vaccin']
        if len(searched) != 0:
            all_vaccins = Vaccin.objects.filter(
                Q(protects_against__icontains=searched) | Q(vaccin_name__icontains=searched)
            ).values()

    context = {
        'vaccins': all_vaccins,
        'booster_alert': booster_alert
    }
    return render(request, 'vaccinationmanagement/vaccins.html', context)

@user_passes_test(lambda u: u.groups.filter(name='patient').exists(), login_url='index')
def private(request):
    """
    Startpage for private person
    """
    booster_alert = alert_if_booster(request)
    patient = User.objects.get(id=request.user.id).patient_set.all().values()[0]
    context = {
        "patient": patient,
        'booster_alert': booster_alert
    }
    return render(request, 'vaccinationmanagement/private.html', context)

@user_passes_test(lambda u: u.groups.filter(name='patient').exists(), login_url='index')
def private_vaccinations(request):
    """
    Shows private persons vaccinations and enables search among vaccinations
    """
    booster_alert = alert_if_booster(request)
    patient = User.objects.get(id=request.user.id).patient_set.first()
    patient_id=getattr(patient, 'patient_id')
    vaccinations = Vaccination.objects.filter(
        patient_id=patient_id
    ).select_related('vaccin').order_by('vaccin')
    grouped_vaccinations = check_for_booster(group_vaccinations(vaccinations))
    if request.method == "POST":
        searched = request.POST['search-vaccinations']
        if len(searched) != 0:
            searched_vaccinations = Vaccination.objects.filter(
                patient_id=patient_id, vaccin__vaccin_name__icontains=searched
            )
            grouped_vaccinations = check_for_booster(group_vaccinations(searched_vaccinations))

    context = {
        'patient_id': patient_id,
        'patient' : patient,
        'vaccinations' : grouped_vaccinations,
        'booster_alert': booster_alert
    }

    return render(request, 'vaccinationmanagement/vaccinations.html', context)

def login_staff(request):
    """
    Login as staff
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name="staff").exists():
                login(request, user)
                return redirect("staff/home")
            messages.error(
                request,
                'This user is not registered as Staff. Try login in as Private Person.'
            )
            return render(
                request,
                "vaccinationmanagement/index.html",
                {'form': form, 'staff_login': 'staff-login'}
            )
    else:
        form = AuthenticationForm()
    return render(
        request,
        "vaccinationmanagement/index.html",
        {'form': form, 'staff_login': 'staff-login'}
    )

def login_private(request):
    """
    Login as private person
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name="patient").exists():
                login(request, user)
                return redirect("private/home")
            messages.error(
                request,
                'This user is not registered as a Private Person. Try login in as Staff.'
            )
            return render(
                request,
                "vaccinationmanagement/index.html",
                {'form': form, 'private_login': 'private-login'}
            )
    else:
        form = AuthenticationForm()
    return render(
        request,
        "vaccinationmanagement/index.html",
        {'form': form, 'private_login': 'private-login'}
    )

def logout_user(request):
    """
    Logout
    """
    if request.method == "POST":
        logout(request)
        return redirect("index")
    return redirect("index")
