from django.core.mail import send_mail
from django.conf import settings
from api.models import Notification
from notifications_management.notification_level.notification_level import NotificationLevel
from notifications_management.notification_sender.notification_sender import NotificationSender


class EmailNotificationSender(NotificationSender):

    def __init__(self, level: NotificationLevel):
        """
         Initialize the EmailNotificationSender with a NotificationLevel.

         Args:
             level (NotificationLevel): The level of notification to be used.
         """
        super().__init__(level)

    def get_recipient(self, notification: Notification):
        """
        Get the recipient email address for the notification.

        This method retrieves the email address of the caregiver associated with the notification.

        Args:
            notification (Notification): The notification object containing information about the alert.

        Returns:
            str: The email address of the recipient caregiver.
        """
        recipient = notification.caregiver.caregiver.email
        return recipient

    def send(self, subject, content, recipient):
        """
        Send the notification email.

        This method sends the notification email to the recipient caregiver.

        Args:
            subject (str): The subject line of the email.
            content (str): The content/body of the email.
            recipient (str): The email address of the recipient.
        """
        send_mail(
            subject=subject,
            message=content,
            from_email=settings.EMAIL_FROM,
            recipient_list=[recipient],
            fail_silently=False,
        )
