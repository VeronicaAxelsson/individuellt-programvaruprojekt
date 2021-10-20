"""
Models
"""
from django.db import models
from django.contrib.auth.models import User

class Vaccin(models.Model):
    """
    Vaccine table
    """
    vaccin_id = models.BigAutoField(primary_key=True)
    vaccin_name = models.CharField(max_length=255)
    protects_against = models.CharField(max_length=255)
    info_url = models.CharField(max_length=255)

    def __str__(self):
        return self.vaccin_name

class Patient(models.Model):
    """
    Patient table
    """
    patient_id = models.BigAutoField(primary_key=True)
    social_security_nr = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    adress = models.CharField(max_length=50)
    tel_nr = models.IntegerField()
    email = models.CharField(max_length=50)
    belong_to_users = models.ManyToManyField(User)

class Vaccination(models.Model):
    """
    Vaccination table
    """
    vaccination_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, related_name='patient', on_delete=models.CASCADE)
    vaccin = models.ForeignKey(Vaccin, related_name='vaccin', on_delete=models.CASCADE)
    dose_nr = models.IntegerField()
    date_of_vaccination = models.DateField()
    date_of_next_vaccination = models.DateField(default='NULL', null=True)
    vaccination_done = models.BooleanField()
    note = models.CharField(max_length=255, default='NULL')
