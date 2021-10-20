from django.contrib.auth.models import User
from vaccinationmanagement.models import Vaccin, Patient, Vaccination
import datetime

def check_for_booster(vaccinations):
    """
    Takes a list of vaccinations, groups them, loops through the vaccinations
    and gets the latest vaccination of each kind. Then checks the timedifference
    between now and next dose, and in that sets upcomming_booster till True.
    """
    for vaccin in vaccinations:
        latest_vaccination = get_latest_dose(vaccinations.get(vaccin))
        if latest_vaccination.date_of_next_vaccination is not None:
            time_differnce = (latest_vaccination.date_of_next_vaccination - datetime.date.today()).days
            if time_differnce <= 30:
                latest_vaccination.uppcomming_booster = True
    return vaccinations

def check_if_patient_has_booster(vaccinations):
    """
    Takes a list of vaccinations, groups them, loops through the vaccinations
    and gets the latest vaccination of each kind. Then checks the timedifference
    between now and next dose.
    """
    vaccinations = group_vaccinations(vaccinations)
    for vaccin in vaccinations:
        latest_vaccination = get_latest_dose(vaccinations.get(vaccin))
        # if latest_vaccination is None:
        #     return False
        if latest_vaccination.date_of_next_vaccination is not None:
            time_differnce = (latest_vaccination.date_of_next_vaccination - datetime.date.today()).days
            if time_differnce <= 30:
                return True
    return False

def alert_if_booster(request):
    """
    Takes a request, fetches the users patients, loops through the patients,
    and checks if there are any upcomming booster vaccinations.
    """
    patients = User.objects.get(id=request.user.id).patient_set.all()
    for patient in patients:
        vaccinations = Vaccination.objects.filter(patient__patient_id=patient.patient_id).select_related('vaccin')
        if check_if_patient_has_booster(vaccinations):
            return True
    return False

def get_latest_dose(vaccination):
    """
    Takes list with vaccinations and returns the vaccination
    with highest dose number
    """
    current_vaccination = None
    for vaccin in vaccination:
        if current_vaccination is None:
            current_vaccination = vaccin
            continue
        if vaccin.dose_nr > current_vaccination.dose_nr:
            current_vaccination = vaccin
    return current_vaccination

def group_vaccinations(vaccinations):
    grouped_vaccinations = {}
    for vaccination in vaccinations:
        vaccin_id = vaccination.vaccin_id
        if vaccin_id in grouped_vaccinations:
            grouped_vaccinations[vaccin_id].append(vaccination)
        else:
            grouped_vaccinations[vaccin_id] = [vaccination]
    return grouped_vaccinations
