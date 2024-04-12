import threading
from api.models import SensorAlert, CaregiverLevel
from chain_of_responsibility.handlers.base_handler import BaseHandler
from abc import ABC, abstractmethod
from notifications_management.notification_level.notification_level_three import NotificationLevelThree
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender


class GenericCaregiverHandler(BaseHandler, ABC):
    """
    An abstract base class for handlers that send notifications to caregivers.

    This class provides common functionality for sending notifications to caregivers,
    such as generating notifications and tracking the notifications that have been sent.

    Subclasses must implement the `get_caregivers` method to retrieve the caregivers
    that should receive notifications.
    """

    WAIT_TIME = CaregiverLevel._meta.get_field('wait_time').default

    def handle(self, request: SensorAlert) -> None:
        """
        Handles a sensor alert by sending notifications to the appropriate caregivers.

        :param request: The sensor alert to handle.
        """

        # Get all the rows in the table 'Caregiver' related to the elderly person and the level of help
        caregivers = self.get_caregivers(request)

        if caregivers is not None:

            for caregiver in caregivers:
                # print(caregiver)
                notification = BaseHandler.build_notification(caregiver, request)
                self._generated_notifications.add(notification)

                EmailNotificationSender(NotificationLevelThree()).deliver_notification(notification)

            # Build & start the timer
            self._timer = threading.Timer(self.WAIT_TIME, lambda: self.timer_callback(request))
            self._timer.start()

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
