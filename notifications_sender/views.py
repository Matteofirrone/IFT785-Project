# Dans votre fichier models.py ou un fichier séparé, par exemple, notifications.py

from abc import ABC, abstractmethod
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from api.models import Notification, Caregiver, Person, SensorAlert


class NotificationSender(ABC):
    # Méthode pour livrer la notification
    def deliver_notification(self, notification):

        # TODO
        # RECEVOIR LES DONNEES

        # Générer la notification complète
        full_notification = self.build_notification(notification)
        # Envoyer la notification
        self.send_notification(full_notification)
    @abstractmethod
    def build_notification(self, notification: Notification):
        pass

    @abstractmethod
    def generate_subject(self, notification: Notification) -> str:
        pass

    @abstractmethod
    def generate_body(self, notification: Notification) -> str:
        pass

    @abstractmethod
    def send_notification(self, notification: Notification):
        pass

class EmailNotificationSender(NotificationSender):

    def generate_subject(self, notification):
        try:
            # Récupérer l'objet Caregiver associé à la notification
            caregiver = Caregiver.objects.get(id=notification.caregiver)
            # Récupérer l'objet Person représentant la personne âgée associée au soignant
            elderly_person = Person.objects.get(id=caregiver.elderly)
            # Récupérer le nom de la personne âgée
            elderly_name = f"{elderly_person.first_name} {elderly_person.last_name}"
            return f"{elderly_name} a besoin d'aide"
        except ObjectDoesNotExist:
            return "Notification associée à un soignant inexistant"

    def generate_body(self, notification):
        caregiver_person = Person.objects.get(id=notification.caregiver)
        sensort_alert = SensorAlert.objects.get(id=notification.sensor_alert)
        return f"{caregiver_person.first_name} {caregiver_person.last_name} {sensort_alert.subject}"

    def build_notification(self, notification):
        subject = self.generate_subject(notification)
        body = self.generate_body(notification)
        return f"Sujet: {subject}\n\nCorps: {body}"

    def send_notification(self, notification: Notification):
        send_mail(
            subject=self.generate_subject(notification),
            message=self.generate_body(notification),
            from_email="",
            recipient_list=[''],
        )

