# Dans votre fichier models.py ou un fichier séparé, par exemple, notifications.py

from abc import ABC, abstractmethod
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from email.message import EmailMessage
import smtplib
from django.core.serializers.python import Serializer

from api.models import Notification, Caregiver, Person, SensorAlert
from ift785_project import settings


class NotificationSender(ABC):
    # Méthode pour livrer la notification
    def deliver_notification(self, notification):
        # TODO
        # RECEVOIR LES DONNEES
        return ""

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
        # TODO - Acces "subject" from notification.sensor_alert
        subject = notification.sensor_alert.subject
        return f"{subject}"

    def generate_body(self, notification):
        # TODO - Access "Datas" from notification.sensor_alert
        start = notification.sensor_alert.start
        location = notification.sensor_alert.location
        state = notification.sensor_alert.state
        measurable = notification.sensor_alert.measurable
        home = notification.sensor_alert.home
        body = (f"Home : {home} \n"
                f"Location : {location} \n"
                f"Start : {start} \n"
                f"State : {state} \n"
                f"Measurable : {measurable}")
        return f"{body}"

    def build_notification(self, notification):
        # TODO - Useless ?
        return ""

    def send_notification(self, notification: Notification):
        msg = EmailMessage()
        # TODO - Access to "email" from notification.caregiver
        msg["to"] = notification.caregiver.email
        msg["from"] = settings.EMAIL_HOST
        msg["Subject"] = self.generate_subject(notification)
        msg.set_content(self.generate_body(notification))

        with smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT) as smtp:
            smtp.login(settings.EMAIL_HOST, settings.EMAIL_PASSWORD)

            # Send Mail
            smtp.send_message(msg)
            print("SUCCESS !")

