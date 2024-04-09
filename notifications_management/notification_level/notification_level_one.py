from api.models import Notification
from notifications_management.notification_level.notification_level import NotificationLevel
from notifications_management.notification_sender.notification_sender import NotificationSender


class NotificationLevelOne(NotificationLevel):

    def generate_content(self, notification: Notification):
        elderly = notification.caregiver.elderly
        sensor_alert = notification.sensor_alert

        content = (
            f"Dear {elderly.first_name} {elderly.last_name},\n\n"
            f"We request your attention because a new alert has been triggered. \n"
            f"Details : "
            f"Start: {sensor_alert.start}\n"
            f"Location: {sensor_alert.location}\n"
            f"State: {sensor_alert.state}\n"
            f"Measurable: {sensor_alert.measurable}\n\n"
            f"Please click on the following link to confirm "
            f"that you have received this notification"
            f"Confirmation link: {NotificationSender.generate_link(notification)}\n\n"
            f"Best regards,\n"
            f"IFT785 Project Team"
        )
        return content

    def generate_subject(self, notification: Notification):
        sensor_alert = notification.sensor_alert
        elderly = notification.caregiver.elderly
        subject = f"Alert detected for {elderly.first_name} {elderly.last_name} ({sensor_alert.location})"
        return subject