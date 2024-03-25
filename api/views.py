from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import SensorAlert
from .serializers import SensorAlertSerializer

from rest_framework import viewsets


class SensorAlertViewSet(viewsets.ModelViewSet):
    queryset = SensorAlert.objects.all()
    serializer_class = SensorAlertSerializer

    # Allow GET, POST, PUT, and DELETE requests
    # (adjust as needed for your specific API)
    http_method_names = ['get', 'post', 'put', 'delete']