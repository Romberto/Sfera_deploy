from django.urls import path

from . import views

urlpatterns = [
    path('', views.DriversView.as_view(), name='drivers')
]