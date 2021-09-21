from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, 'vaccinationmanagement/index.html')

def staff(request):
    return HttpResponse("Staff home page.")

def patients(request):
    return HttpResponse("List of patients.")

def patient_vaccinations(request, patient_id):
    # template = loader.get_template('vaccinationmanagement/patient.html')
    context = {
        'patient_id' : patient_id,
    }
    return render(request, 'vaccinationmanagement/patient.html', context)

def vaccins(request):
    return HttpResponse("List of all vaccins, with links to read about them.")

def private(request):
    return HttpResponse("Private person home page.")

def vaccinations(request):
    return HttpResponse("Private persons own vaccinations")
