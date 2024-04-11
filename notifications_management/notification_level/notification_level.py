from abc import ABC, abstractmethod

from api.models import Notification


class NotificationLevel(ABC):

    @abstractmethod
    def generate_content(self, notification: Notification):
        """
        Generate the content/body of the notification.

        This method should be implemented by concrete subclasses.

        Args:
            notification (Notification): The notification object.

        Returns:
            str: The content/body of the notification.
        """
        pass

    @abstractmethod
    def generate_subject(self, notification: Notification):
        """
        Generate the subject line of the notification.

        This method should be implemented by concrete subclasses.

        Args:
            notification (Notification): The notification object.

        Returns:
            str: The subject line of the notification.
        """
        pass