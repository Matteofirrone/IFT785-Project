from django.urls import path, include
from rest_framework import routers
from .views import SensorAlertView


urlpatterns = [
    path('alert', SensorAlertView.as_view()),
]
