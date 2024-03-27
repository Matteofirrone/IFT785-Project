from threading import Thread

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chain_of_responsibility.initializer import ApplicationInitializer
from .serializers import SensorAlertSerializer
from .models import SensorAlert


def throw_in_chain(sensor_alert: SensorAlert) -> None:
    # Get an instance of the Singleton
    initializer_instance = ApplicationInitializer()
    # Throw the alert into the chain
    initializer_instance.get_chain_of_responsibility().handle(sensor_alert)


class SensorAlertView(APIView):
    def post(self, request, format=None):
        serializer = SensorAlertSerializer(data=request.data)
        if serializer.is_valid():
            sensor_alert = serializer.save()

            # Start a new thread to handle the chain
            chain_thread = Thread(target=throw_in_chain, args=(sensor_alert,))
            chain_thread.start()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
