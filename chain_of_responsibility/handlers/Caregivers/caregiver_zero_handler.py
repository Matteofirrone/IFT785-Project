import threading
from api.models import SensorAlert, Caregiver, CaregiverLevel
from chain_of_responsibility.handlers.base_handler import BaseHandler
from notifications_management.notification_level.notification_level_one import NotificationLevelOne
from notifications_management.notification_level.notification_level_two import NotificationLevelTwo
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender


class CaregiverZeroHandler(BaseHandler):
    """
    Handler for caregivers with level 0.

    This handler is responsible for handling requests for caregivers with level 0.
    If the request cannot be handled by this handler, it will pass the request to the next handler in the chain.
    """

    WAIT_TIME = CaregiverLevel.objects.get(level=0).wait_time

    def handle(self, request: SensorAlert):
        """
        Handles the incoming request.

        If the caregiver exists, it will build a notification for the caregiver with level 0
        and send it. If the caregiver is not found, it will pass the request to the next handler
        in the chain.

        Args:
            request: The request to be handled.
        """
        # Get the caregiver
        caregiver = self.get_caregiver(request)

        if caregiver is not None:

            # print(caregiver)
            notification = BaseHandler.build_notification(caregiver, request)
            self._generated_notifications.add(notification)
            EmailNotificationSender(NotificationLevelOne()).deliver_notification(notification)

            # Build & start the timer
            self._timer = threading.Timer(self.WAIT_TIME, lambda: self.timer_callback(request, notification))
            self._timer.start()
        else:
            # Pass the request to the next handler
            super().handle(request)

    def get_caregiver(self, request: SensorAlert) -> Caregiver:
        """
        Gets the caregiver associated with the request.

        Args:
            request: The request to be handled.

        Returns:
            The caregiver associated with the request.
        """
        return Caregiver.objects.get(elderly=request.home.elderly, caregiver=request.home.elderly, level__level=0)

    def timer_callback(self, request, notification):
        """
        Callback function for the timer.

        This function is called when the timer expires. It sends a second notification and starts a second timer.

        Args:
            request: The request associated with the notification.
            notification: The notification to be sent.
        """
        EmailNotificationSender(NotificationLevelTwo()).deliver_notification(notification)
        self._timer = threading.Timer(self.WAIT_TIME - 20, lambda: self.second_timer_callback(request))
        self._timer.start()

    def second_timer_callback(self, request):
        """
        Callback function for the second timer.

        This function is called when the second timer expires. It passes the request to the next handler in the chain.

        Args:
            request: The request associated with the notification.
        """
        super().handle(request)
