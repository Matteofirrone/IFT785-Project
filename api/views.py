from threading import Thread
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from chain_of_responsibility.chain_manager import ChainManager
from chain_of_responsibility.signals import notification_accepted, help_requested
from .serializers import SensorAlertSerializer
from .models import SensorAlert, Notification


def throw_in_chain(sensor_alert: SensorAlert) -> None:
    """
    Throw the given SensorAlert into a new chain of responsibility.

    This function gets the instance of the ChainManager and calls the handle method of the chain of responsibility
    with the given SensorAlert as the argument.

    :param sensor_alert: The SensorAlert to be thrown into the chain of responsibility.
    """

    # Get the instance of the ChainManager
    chain_manager = ChainManager()
    # Throw the alert into a new chain
    chain_manager.get_chain_of_responsibility().handle(sensor_alert)


class SensorAlertView(APIView):
    """
    A view to handle the creation of SensorAlerts.
    """
    def post(self, request, format=None):
        """
        Create a new SensorAlert and throw it into a new chain of responsibility.

        This method validates the request data using the SensorAlertSerializer, saves the validated data as a new
        SensorAlert, and starts a new thread to throw the SensorAlert into a new chain of responsibility.
        """
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
    """
    Confirm a Notification and dispatch the appropriate signal.

    This method gets the token and help_requested parameters from the GET request, retrieves the corresponding
    Notification object, and dispatches the appropriate signal (notification_accepted or help_requested) based on the
    value of the help_requested parameter.
    """
    token = request.GET.get('token')
    is_help_requested = request.GET.get('help_requested') == 'true'
    notification = get_object_or_404(Notification, token=token)

    if is_help_requested:
        help_requested.send(sender=confirm_notification, notification=notification)
        return HttpResponse("Your request for assistance has been transmitted and someone will come to help you soon")
    # Check whether the sensor alert associated with this notification has already been resolved.
    elif not notification.sensor_alert.is_resolved:
        # Dispatch the signal
        notification_accepted.send(sender=confirm_notification, notification=notification)
        return HttpResponse(f"Request for assistance accepted : please proceed with the necessary actions for {notification.caregiver.elderly.first_name}")
    else:
        return HttpResponse(f"The request for assistance has already been accepted : assistance is currently in progress for {notification.caregiver.elderly.first_name}")
