from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Patient, Vaccin, Vaccination

# Register out own model admin, based on the default UserAdmin
# @admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


# Unregister the provided model admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Vaccin)
admin.site.register(Vaccination)
