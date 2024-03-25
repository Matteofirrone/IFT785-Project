from rest_framework import serializers
from api.models import SensorAlert


class SensorAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorAlert
        fields = '__all__'
