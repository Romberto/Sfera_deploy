from django.db import models

from drivers.models import DriverModel
from excursions.models import ExcursionModel


class TokenExModel(models.Model):
    active = models.BooleanField(default=True)  # активный или нет токен
    phone = models.CharField(max_length=30, null=True, blank=True)
    body = models.CharField(max_length=20)  # тело токена(сам код)
    date_create = models.DateTimeField(auto_now=True)  # время создания токена
    date_activate = models.DateTimeField(null=True, blank=True)  # время активации токена
    driver_activate = models.ForeignKey(DriverModel, on_delete=models.CASCADE, null=True,
                                        blank=True)  # водитель-экскурсовод который активировал токен
    excursion = models.ForeignKey(ExcursionModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.body)

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"
