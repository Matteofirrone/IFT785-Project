from threading import Thread
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from chain_of_responsibility.initializer import ApplicationInitializer
from chain_of_responsibility.signals import notification_accepted
from .serializers import SensorAlertSerializer
from .models import SensorAlert, Notification


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


@require_GET
def confirm_notification(request):
    token = request.GET.get('token')
    notification = get_object_or_404(Notification, token=token)
    notification.has_accepted = True
    notification.save()

    # Dispatch the signal
    notification_accepted.send(sender=confirm_notification, notification=notification)

    return HttpResponse("Notification accepted.")
