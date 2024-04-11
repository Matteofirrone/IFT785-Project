from abc import ABC, abstractmethod
from django.urls import reverse
from api.models import Notification
from ift785_project import settings
from notifications_management.notification_level.notification_level import NotificationLevel


class NotificationSender(ABC):

    def __init__(self, level: NotificationLevel):
        """
        Abstract base class for notification senders.

        This class defines the interface for sending notifications and provides methods for generating
        email content, subject, and recipient.

        Args:
            level (NotificationLevel): The level of notification to be used.
        """
        self.level = level

    @property
    def level(self):
        """
        Get the level of notification.

        Returns:
            NotificationLevel: The level of notification.
        """
        return self._level

    @level.setter
    def level(self, value):
        """
        Set the level of notification.

        Args:
            value (NotificationLevel): The level of notification to be set.
        """
        self._level = value

    @staticmethod
    def generate_link(notification: Notification):
        """
        Generate the confirmation link for the notification.

        Args:
            notification (Notification): The notification object.

        Returns:
            str: The confirmation link for the notification.
        """
        token = notification.token
        url = reverse('api:confirm_notification')
        domain = settings.DOMAIN
        return f"{domain}{url}?token={token}"

    def deliver_notification(self, notification: Notification):
        """
         Deliver the notification.

         This method generates the content, subject, and recipient of the notification
         and then sends the notification.

         Args:
             notification (Notification): The notification object.
         """
        content = self.generate_content(notification)
        subject = self.generate_subject(notification)
        recipient = self.get_recipient(notification)
        self.send(subject=subject, content=content, recipient=recipient)

    def generate_content(self, notification: Notification):
        """
        Generate the content/body of the notification email.

        This method should be implemented by concrete subclasses.

        Args:
            notification (Notification): The notification object.

        Returns:
            str: The content/body of the notification email.
        """
        if self.level is None:
            raise ValueError("Level is not set")
        return self.level.generate_content(notification)

    def generate_subject(self, notification: Notification):
        """
        Generate the subject line of the notification email.

        This method should be implemented by concrete subclasses.

        Args:
            notification (Notification): The notification object.

        Returns:
            str: The subject line of the notification email.
        """
        if self.level is None:
            raise ValueError("Level is not set")
        return self.level.generate_subject(notification)

    @abstractmethod
    def get_recipient(self, notification: Notification):
        """
        Get the recipient email address for the notification.

        This method should be implemented by concrete subclasses.

        Args:
            notification (Notification): The notification object.

        Returns:
            str: The email address of the recipient.
        """
        pass

    @abstractmethod
    def send(self, subject, content, recipient):
        """
        Send the notification email.

        This method should be implemented by concrete subclasses.

        Args:
            subject (str): The subject line of the email.
            content (str): The content/body of the email.
            recipient (str): The email address of the recipient.
        """
        pass
