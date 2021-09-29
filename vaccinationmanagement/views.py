from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from vaccinationmanagement.models import Vaccin, Patient, Vaccination
from django.forms.models import model_to_dict

def index(request):
    return render(request, 'vaccinationmanagement/index.html', {'start_page': 'start-page'})

def staff(request):
    return render(request, 'vaccinationmanagement/staff.html')

def patients(request):
    return render(request, 'vaccinationmanagement/patients.html')

def patient_vaccinations(request, patient_id):
    # template = loader.get_template('vaccinationmanagement/patient.html')
    context = {
        'patient_id' : patient_id,
    }
    return render(request, 'vaccinationmanagement/patient.html', context)

def add_dose(request, patient_id, vaccination_id):
    context = {
        'patient_id' : patient_id,
        'vaccination_id': vaccination_id
    }
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/patient.html', context)
    else:
        return render(request, 'vaccinationmanagement/forms/add-dose.html', context)

def add_patient(request):
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/patients.html')
    else:
        return render(request, 'vaccinationmanagement/forms/add-patient.html')

def add_vaccination(request, patient_id):
    context = {
        'patient_id' : patient_id
    }
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/patient.html', context)
    else:
        return render(request, 'vaccinationmanagement/forms/add-vaccination.html')

def search_patient(request, patient_id):
    context = {
        'patient_id' : patient_id
    }
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/patient.html', context)

def search_vaccin(request, vaccin_id):
    context = {
        'vaccin_id' : vaccin_id
    }
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/vaccins.html', context)

def search_vaccination(request, patient_id):
    context = {
        'patient_id': patient_id
    }
    if request.method == "POST":
        return render(request, 'vaccinationmanagement/patient.html', context)

def vaccins(request):
    context = {}
    all_vaccins = Vaccin.objects.all().values()
    context['data'] = all_vaccins
    return render(request, 'vaccinationmanagement/vaccins.html', context)

def private(request):
    return HttpResponse("Private person home page.")

def vaccinations(request):
    return HttpResponse("Private persons own vaccinations")

from django.contrib.auth import authenticate, login

def login_staff(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("staff/home")
    else:
        form = AuthenticationForm()
    return render(request, "vaccinationmanagement/index.html", {'form': form, 'staff_login': 'staff-login'})

def login_private(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("private/home")
    else:
        form = AuthenticationForm()
    return render(request, "vaccinationmanagement/index.html", {'form': form, 'private_login': 'private-login'})

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")
