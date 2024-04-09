from abc import ABC, abstractmethod
from django.urls import reverse
from api.models import Notification
from ift785_project import settings
from notifications_management.notification_level.notification_level import NotificationLevel


class NotificationSender(ABC):

    def __init__(self, level: NotificationLevel):
        self.level = level

    @staticmethod
    def generate_link(notification: Notification):
        token = notification.token
        url = reverse('api:confirm_notification')
        domain = settings.DOMAIN
        return f"{domain}{url}?token={token}"

    def deliver_notification(self, notification: Notification):
        content = self.level.generate_content(notification)
        subject = self.level.generate_subject(notification)
        recipient = self.get_recipient(notification)
        self.send(subject=subject, content=content, recipient=recipient)

    @abstractmethod
    def generate_content(self, notification: Notification):
        pass

    @abstractmethod
    def generate_subject(self, notification: Notification):
        pass

    @abstractmethod
    def get_recipient(self, notification: Notification):
        pass

    @abstractmethod
    def send(self, subject, content, recipient):
        pass
