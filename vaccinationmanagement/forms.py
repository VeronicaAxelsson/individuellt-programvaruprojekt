from django import forms
from . import models

class AddVaccination(forms.ModelForm):
    class Meta:
        model = models.Vaccination
        fields = ['vaccin', 'dose_nr', 'date_of_vaccination', 'date_of_next_vaccination', 'vaccination_done', 'note']
