import bcrypt
from django.shortcuts import render
from django.views import View

from drivers.models import DriverModel


class DriversView(View):

    def get(self, request):
        drivers = DriverModel.objects.all()
        pas = '123456'
        hashed = bcrypt.hashpw(pas.encode('utf-8'), bcrypt.gensalt())
        for item in drivers:
            print(item.password, '  ', str(hashed))
            if item.password == str(hashed):
                print(item.password)
        return render(request, 'drivers/drivers.html')

