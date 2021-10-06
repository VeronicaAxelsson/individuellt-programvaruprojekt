from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from vaccinationmanagement.models import Vaccin, Patient, Vaccination
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from vaccinationmanagement.forms import AddVaccination
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

def index(request):
    if request.user.groups.filter(name="staff").exists():
        return redirect('staff')
    if request.user.groups.filter(name="patient").exists():
        return redirect('private')
    return render(request, 'vaccinationmanagement/index.html', {'start_page': 'start-page'})

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def staff(request):
    permission = request.user.groups.filter(name="staff").exists()
    print(permission)
    return render(request, 'vaccinationmanagement/staff.html')

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def patients(request):
    if request.method == "POST":
        searched = request.POST['search-patient']
        if len(searched) != 0:
            searched_patients = User.objects.get(id=request.user.id).patient_set.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched) | Q(social_security_nr__contains=searched)).values()
            context = {
                'searched': searched,
                'searched_patients': searched_patients
            }
            return render(request, 'vaccinationmanagement/patients.html', context)
    staffs_patients = User.objects.get(id=request.user.id).patient_set.all().values()
    context = {
        'data': staffs_patients
    }
    return render(request, 'vaccinationmanagement/patients.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def patient_vaccinations(request, patient_id):
    patient = Patient.objects.filter(patient_id=patient_id).values()[0]
    if request.method == "POST":
        searched = request.POST['search-vaccinations']
        if len(searched) != 0:
            searched_vaccinations = Vaccination.objects.filter(patient__patient_id=patient_id, vaccin__vaccin_name__contains=searched)
            context = {
                'patient_id': patient_id,
                'searched': searched,
                'searched_vaccinations': searched_vaccinations
            }
            return render(request, 'vaccinationmanagement/patient.html', context)
    vaccinations = Vaccination.objects.filter(patient__patient_id=patient_id).select_related('vaccin').order_by('vaccin')
    context = {
        'patient_id' : patient_id,
        'patient' : patient,
        'vaccinations' : vaccinations
    }

    return render(request, 'vaccinationmanagement/patient.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def add_dose(request, patient_id, vaccination_id):
    context = {
        'patient_id' : patient_id,
        'vaccination_id': vaccination_id
    }
    if request.method == "POST":
        dose_nr = request.POST['dose_nr']
        date_of_vaccination = request.POST['date_of_vaccination']
        date_of_next_vaccination = request.POST['date_of_next_vaccination']
        if 'vaccination_done' in request.POST:
            vaccination_done = True
            date_of_next_vaccination = None
        else:
            vaccination_done = False
        ins = Vaccination.objects.filter(vaccination_id=vaccination_id)
        ins.update(dose_nr=dose_nr, date_of_vaccination=date_of_vaccination, date_of_next_vaccination=date_of_next_vaccination, vaccination_done=vaccination_done)
        return redirect('patient', patient_id=patient_id)
    else:
        return render(request, 'vaccinationmanagement/forms/add-dose.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def add_patient(request):
    patients = Patient.objects.all().values()
    context = {
        'patients' : patients
    }
    if request.method == "POST":
        patient_id = request.POST['addPatient']
        print(patient_id)
        Patient.objects.get(patient_id=patient_id).belong_to_users.add(User.objects.get(id=request.user.id))
        return redirect('patients')
    else:
        return render(request, 'vaccinationmanagement/forms/add-patient.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def add_vaccination(request, patient_id):
    context = {
        'patient_id' : patient_id
    }
    if request.method == "POST":
        # form = AddVaccination(request.POST)
        # if form_is_valid():
        #     pass
        print(request.POST)
        vaccin = Vaccin.objects.get(vaccin_id=request.POST['vaccin'])
        dose_nr = request.POST['dose_nr']
        date_of_vaccination = request.POST['date_of_vaccination']
        date_of_next_vaccination = request.POST['date_of_next_vaccination']
        patient = Patient.objects.get(patient_id=request.POST['patient'])
        if 'vaccination_done' in request.POST:
            vaccination_done = True
            date_of_next_vaccination = None
        else:
            vaccination_done = False
        ins = Vaccination(vaccin=vaccin, dose_nr=dose_nr, date_of_vaccination=date_of_vaccination, date_of_next_vaccination=date_of_next_vaccination, patient=patient, vaccination_done=vaccination_done)
        ins.save()
        return redirect('patient', patient_id=patient_id)
    else:
        vaccins = Vaccin.objects.all()
        # form = AddVaccination()
        context = {
            'patient_id' : patient_id,
            'vaccins': vaccins
        }
        return render(request, 'vaccinationmanagement/forms/add-vaccination.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def search_patient(request, patient_id):
    context = {
        'patient_id' : patient_id
    }
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/patient.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def search_vaccin(request, vaccin_id):
    context = {
        'vaccin_id' : vaccin_id
    }
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/vaccins.html', context)

@user_passes_test(lambda u: u.groups.filter(name='staff').exists(), login_url='index')
def vaccins(request):
    if request.method == "POST":
        searched = request.POST['search-vaccin']
        if len(searched) != 0:
            searched_vaccins = Vaccin.objects.filter(vaccin_name__contains=searched).values()
            context = {
                'searched': searched,
                'searched_vaccins': searched_vaccins
            }
            return render(request, 'vaccinationmanagement/vaccins.html', context)
    all_vaccins = Vaccin.objects.all().values()
    context = {
        'data': all_vaccins
    }
    return render(request, 'vaccinationmanagement/vaccins.html', context)

@user_passes_test(lambda u: u.groups.filter(name='patient').exists(), login_url='index')
def private(request):
    return render(request, 'vaccinationmanagement/private.html')

@user_passes_test(lambda u: u.groups.filter(name='patient').exists(), login_url='index')
def vaccinations(request):
    patient = User.objects.get(id=request.user.id).patient_set.first()
    patient_id=getattr(patient, 'patient_id')
    if request.method == "POST":
        searched = request.POST['search-vaccinations']
        if len(searched) != 0:
            searched_vaccinations = Vaccination.objects.filter(patient_id=patient_id, vaccin__vaccin_name__contains=searched)
            context = {
                'patient_id': patient_id,
                'searched': searched,
                'searched_vaccinations': searched_vaccinations
            }
            return render(request, 'vaccinationmanagement/vaccinations.html', context)
    vaccinations = Vaccination.objects.filter(patient_id=patient_id).select_related('vaccin').order_by('vaccin')
    context = {
        'patient_id': patient_id,
        'patient' : patient,
        'vaccinations' : vaccinations
    }

    return render(request, 'vaccinationmanagement/vaccinations.html', context)

def login_staff(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name="staff").exists():
                login(request, user)
                return redirect("staff/home")
            else:
                messages.error(request,'This user is not registered as Staff. Try login in as Private Person.')
                return render(request, "vaccinationmanagement/index.html", {'form': form, 'staff_login': 'staff-login'})
    else:
        form = AuthenticationForm()
    return render(request, "vaccinationmanagement/index.html", {'form': form, 'staff_login': 'staff-login'})

def login_private(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name="patient").exists():
                login(request, user)
                return redirect("private/home")
            else:
                messages.error(request,'This user is not registered as a Private Person. Try login in as Staff.')
                return render(request, "vaccinationmanagement/index.html", {'form': form, 'private_login': 'private-login'})
    else:
        form = AuthenticationForm()
    return render(request, "vaccinationmanagement/index.html", {'form': form, 'private_login': 'private-login'})

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")
