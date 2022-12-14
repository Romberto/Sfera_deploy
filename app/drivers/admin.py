from django.contrib import admin
from .models import DriverModel, DriverAdminGroupModel

admin.site.register(DriverModel)
admin.site.register(DriverAdminGroupModel)
