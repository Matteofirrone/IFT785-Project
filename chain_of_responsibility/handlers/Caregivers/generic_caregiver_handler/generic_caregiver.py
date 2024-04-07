import threading
from api.models import Notification, Caregiver, SensorAlert
from chain_of_responsibility.handlers.base_handler import BaseHandler
from abc import ABC, abstractmethod
import uuid
from chain_of_responsibility.signals import notification_accepted
from ift785_project import settings
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender


class GenericCaregiverHandler(BaseHandler, ABC):
    """
    An abstract base class for handlers that send notifications to caregivers.

    This class provides common functionality for sending notifications to caregivers,
    such as generating notifications and tracking the notifications that have been sent.

    Subclasses must implement the `get_caregivers` method to retrieve the caregivers
    that should receive notifications.
    """

    WAIT_TIME = settings.DEFAULT_CAREGIVER_WAIT_TIME

    @staticmethod
    def build_notification(caregiver: Caregiver, sensor_alert: SensorAlert) -> Notification:
        """
        Builds a new notification for the given caregiver and sensor alert.

        :param caregiver: The association between an elderly_person and a caregiver.
        :param sensor_alert: The sensor alert that triggered the notification.
        :return: The new notification.
        """
        notification = Notification(caregiver=caregiver, sensor_alert=sensor_alert, token=GenericCaregiverHandler.generate_token())
        notification.save()
        return notification

    @staticmethod
    def generate_token() -> str:
        """
        Generates a unique token for a notification.

        :return: A unique token.
        """
        token = str(uuid.uuid4())

        # Check if the UUID already exists
        while Notification.objects.filter(token=token).exists():
            token = str(uuid.uuid4())

        return token

    def __init__(self, head_of_chain):
        """
        Initializes a new instance of the `GenericCaregiverHandler` class.
        """
        super().__init__(head_of_chain)
        self._timer = None
        # Keeps track of the notifications generated by the Handler.
        self._generated_notifications = set()
        notification_accepted.connect(self.on_notification_accepted)

    def handle(self, request: SensorAlert) -> None:
        """
        Handles a sensor alert by sending notifications to the appropriate caregivers.

        :param request: The sensor alert to handle.
        """

        # Get all the rows in the table 'Caregiver' related to the elderly person and the level of help
        caregivers = self.get_caregivers(request)

        if caregivers is not None:

            # Build & start the timer
            self._timer = threading.Timer(self.WAIT_TIME, lambda: self.timer_callback(request))
            self._timer.start()

            for caregiver in caregivers:
                # print(caregiver)
                notification = GenericCaregiverHandler.build_notification(caregiver, request)
                self._generated_notifications.add(notification)
                EmailNotificationSender().deliver_notification(notification)
        else:
            # Pass the request to the next handler
            super().handle(request)

    @abstractmethod
    def get_caregivers(self, request: SensorAlert) -> list:
        """
       Retrieves the caregivers that should receive notifications for the given sensor alert.

       :param request: The sensor alert to handle.
       :return: A list of caregivers.
       """
        pass

    def timer_callback(self, request: SensorAlert) -> None:
        """
        Callback function that is called when the timer expires.

        :param request: The sensor alert that triggered the timer.
        """
        super().handle(request)

    def on_notification_accepted(self, *args, **kwargs) -> None:
        """
        Handles a notification acceptance signal.

        :param args: The arguments passed with the signal.
        :param kwargs: The keyword arguments passed with the signal.
        """
        notification = kwargs.get('notification')
        # Check if this notification was sent by this handler
        if notification in self._generated_notifications:
            # Handle the accepted notification
            print(f"Notification {notification.id} has been accepted.")
            self._timer.cancel()
            self.remove_chain()
