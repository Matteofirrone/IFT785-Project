import threading
from api.models import Notification, Caregiver, SensorAlert
from chain_of_responsibility.handlers.base_handler import BaseHandler
from abc import ABC, abstractmethod
import uuid
from chain_of_responsibility.signals import notification_accepted
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender


class GenericCaregiverHandler(BaseHandler, ABC):

    @staticmethod
    def build_notification(caregiver: Caregiver, sensor_alert: SensorAlert) -> Notification:
        notification = Notification(caregiver=caregiver, sensor_alert=sensor_alert, token=GenericCaregiverHandler.generate_token())
        notification.save()
        return notification

    @staticmethod
    def generate_token():
        token = str(uuid.uuid4())

        # Check if the UUID already exists
        while Notification.objects.filter(token=token).exists():
            token = str(uuid.uuid4())

        return token

    def __init__(self):
        super().__init__()
        self._timer = None
        notification_accepted.connect(self.on_notification_accepted)

    def handle(self, request):
        # Get all the rows in the table 'Caregiver' related to the elderly person and the level of help
        caregivers = self.get_caregivers(request)

        if caregivers is not None:

            # Build & start the timer
            self._timer = threading.Timer(60, lambda: self.timer_callback(request))
            self._timer.start()

            for caregiver in caregivers:
                # print(caregiver)
                notification = GenericCaregiverHandler.build_notification(caregiver, request)
                EmailNotificationSender().deliver_notification(notification)
        else:
            # Pass the request to the next handler
            super().handle(request)

    @abstractmethod
    def get_caregivers(self, request):
        pass

    def timer_callback(self, request):
        super().handle(request)
        pass

    def on_notification_accepted(self, *args, **kwargs):
        notification = kwargs.get('notification')
        # Check if this notification was sent by this handler
        if notification.caregiver in self.get_caregivers(notification.sensor_alert):
            # Handle the accepted notification
            print(f"Notification {notification.id} has been accepted.")
            self._timer.cancel()
