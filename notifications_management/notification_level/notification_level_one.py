from api.models import Notification
from notifications_management.notification_level.notification_level import NotificationLevel
from notifications_management.notification_sender.notification_sender import NotificationSender


class NotificationLevelOne(NotificationLevel):

    def generate_content(self, notification: Notification):
        """
         Generate the content of the notification email with level one.

         This method generates the content of the notification email to be sent to the elderly person.

         Args:
             notification (Notification): The notification object containing information about the alert.

         Returns:
             str: The content of the notification email.
         """
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
            f"that you have received this notification\n\n"
            f"Confirmation link: {NotificationSender.generate_link(notification)}\n\n"
            f"If you need help, please click on the following link to request assistance:\n\n"
            f"Help link: {NotificationSender.generate_link(notification)}&help_requested=true\n\n"
            f"Best regards,\n"
            f"IFT785 Project Team"
            f"(This in an alert with level 1)"
        )
        return content

    def generate_subject(self, notification: Notification):
        """
        Generate the subject of the notification email with level one.

        This method generates the subject line of the notification email to be sent to the elderly person.

        Args:
            notification (Notification): The notification object containing information about the alert.

        Returns:
            str: The subject line of the notification email.
        """
        sensor_alert = notification.sensor_alert
        elderly = notification.caregiver.elderly
        subject = f"Alert detected for {elderly.first_name} {elderly.last_name} ({sensor_alert.location})"
        return subject
