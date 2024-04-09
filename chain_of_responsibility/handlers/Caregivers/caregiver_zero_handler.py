import threading

from api.models import SensorAlert, Caregiver
from chain_of_responsibility.handlers.base_handler import BaseHandler
from notifications_management.notification_level.notification_level_one import NotificationLevelOne
from notifications_management.notification_level.notification_level_two import NotificationLevelTwo
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender


class CaregiverZeroHandler(BaseHandler):

    WAIT_TIME = 30

    def handle(self, request: SensorAlert):
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
        return Caregiver.objects.get(elderly=request.home.elderly, caregiver=request.home.elderly, level__level=0)

    def timer_callback(self, request, notification):
        EmailNotificationSender(NotificationLevelTwo()).deliver_notification(notification)
        self._timer = threading.Timer(self.WAIT_TIME - 20, lambda: self.second_timer_callback(request))
        self._timer.start()

    def second_timer_callback(self, request):
        super().handle(request)
