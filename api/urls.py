from django.urls import path, include
from rest_framework import routers
from .views import SensorAlertViewSet

router = routers.DefaultRouter()
router.register('alerts', SensorAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
