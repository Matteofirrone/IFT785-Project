# Dans votre fichier models.py ou un fichier séparé, par exemple, notifications.py

from abc import ABC, abstractmethod
from typing import List
from models import Notification

class NotificationSender(ABC):
    @abstractmethod
    def deliver_notification(self, notification: Notification):
        pass

    @abstractmethod
    def get_contacts(self) -> List[str]:
        pass

    @abstractmethod
    def generate_subject(self, notification: Notification) -> str:
        pass

    @abstractmethod
    def generate_body(self, notification: Notification) -> str:
        pass

    def build_notification(self, notification: Notification):
        subject = self.generate_subject(notification)
        body = self.generate_body(notification)
        return f"{subject}\n\n{body}"

    def send_notification(self, notification: Notification):
        contacts = self.get_contacts()
        formatted_notification = self.build_notification(notification)
        for contact in contacts:
            self.deliver_notification(notification, contact, formatted_notification)

class EmailNotificationSender(NotificationSender):

    def deliver_notification(self, formatted_notification):
        # Logique pour livrer la notification par email
        pass

    def get_contacts(self):
        # Logique pour récupérer les contacts pour les notifications par email
        pass

    def generate_subject(self, notification):
        # Logique pour générer le sujet de la notification par email

        pass

    def generate_body(self, notification):
        # Logique pour générer le corps de la notification par email
        pass
