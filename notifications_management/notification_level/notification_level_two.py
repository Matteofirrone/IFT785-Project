from api.models import Notification
from notifications_management.notification_level.notification_level import NotificationLevel


class NotificationLevelTwo(NotificationLevel):

    def generate_content(self, notification: Notification):
        #TODO generate content for Notification with Level = 2
        return "This is teh content for NotificationLevelTwo"

    def generate_subject(self, notification: Notification):
        # TODO generate subject for Notification with Level = 2
        return "This is teh content for NotificationLevelTwo"