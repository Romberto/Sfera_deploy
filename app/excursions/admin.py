from django.contrib import admin
from .models import ExcursionModel, ExcursionPhoneCodModel, ExcursionPointModel

admin.site.register(ExcursionModel)
admin.site.register(ExcursionPhoneCodModel)
admin.site.register(ExcursionPointModel)
