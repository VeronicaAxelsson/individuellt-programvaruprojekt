from django.db import models

class Vaccin(models.Model):
    vaccin_id = models.BigAutoField(primary_key=True)
    vaccin_name = models.CharField(max_length=255)
    protects_against = models.CharField(max_length=255)
    info_url = models.CharField(max_length=255)

class Patient(models.Model):
    patient_id = models.BigAutoField(primary_key=True)
    social_security_nr = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    adress = models.CharField(max_length=50)
    tel_nr = models.IntegerField()
    email = models.CharField(max_length=50)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

class Vaccination(models.Model):
    vaccination_id = models.BigAutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccin_id = models.ForeignKey(Vaccin, on_delete=models.CASCADE)
    date_of_vaccination = models.DateField()
    date_of_next_vaccination = models.DateField()
    note = models.CharField(max_length=255)
