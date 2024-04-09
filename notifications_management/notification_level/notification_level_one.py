from api.models import Notification
from notifications_management.notification_level.notification_level import NotificationLevel


class NotificationLevelOne(NotificationLevel):

    def generate_content(self, notification: Notification):
        #TODO generate content for Notification with Level = 1
        return "This is teh content for NotificationLevelOne"

    def generate_subject(self, notification: Notification):
        # TODO generate subject for Notification with Level = 1
        return "This is the subject for NotificationLevelOne"