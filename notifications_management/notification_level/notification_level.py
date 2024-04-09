from abc import ABC, abstractmethod

from api.models import Notification


class NotificationLevel(ABC):

    @abstractmethod
    def generate_content(self, notification: Notification):
        pass

    @abstractmethod
    def generate_subject(self, notification: Notification):
        pass