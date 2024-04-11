from api.models import Notification
from notifications_management.notification_level.notification_level import NotificationLevel
from notifications_management.notification_sender.notification_sender import NotificationSender


class NotificationLevelThree(NotificationLevel):

    def generate_content(self, notification: Notification):
        """
         Generate the content of the notification email with level three.

         This method generates the content of the notification email to be sent to the caregiver person.

         Args:
             notification (Notification): The notification object containing information about the alert.

         Returns:
             str: The content of the notification email.
         """
        caregiver = notification.caregiver.caregiver
        elderly = notification.caregiver.elderly
        caregiver_level = notification.caregiver.level.level
        sensor_alert = notification.sensor_alert

        content = (
            f"Dear {caregiver.first_name} {caregiver.last_name},\n\n"
            f"We request your assistance for {elderly.first_name} {elderly.last_name} "
            f"with a caregiver level of {caregiver_level}.\n\n"
            f"Reason: A new alert has been triggered for {elderly.first_name} "
            f"{elderly.last_name} with the following details:\n\n"
            f"Start: {sensor_alert.start}\n"
            f"Location: {sensor_alert.location}\n"
            f"State: {sensor_alert.state}\n"
            f"Measurable: {sensor_alert.measurable}\n\n"
            f"Please click on the following link to confirm "
            f"that you have received this notification and will provide the "
            f"necessary assistance.\n\n"
            f"Confirmation link: {NotificationSender.generate_link(notification)}\n\n"
            f"Best regards,\n"
            f"IFT785 Project Team"
            f"(This in an alert with level 3)"
        )
        return content

    def generate_subject(self, notification: Notification):
        """
        Generate the subject of the notification email with level three.

        This method generates the subject line of the notification email to be sent to the caregiver person.

        Args:
            notification (Notification): The notification object containing information about the alert.

        Returns:
            str: The subject line of the notification email.
        """
        elderly = notification.caregiver.elderly
        caregiver_level = notification.caregiver.level.level
        subject = f"Assistance Requested for {elderly.first_name} {elderly.last_name} - Caregiver Level {caregiver_level}"
        return subject