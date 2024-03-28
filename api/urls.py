from django.urls import path, include
from rest_framework import routers
from .views import SensorAlertView, confirm_notification

urlpatterns = [
    path('alert', SensorAlertView.as_view()),
    path('confirm-notification', confirm_notification),
]
