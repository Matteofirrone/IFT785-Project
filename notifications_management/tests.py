from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from api.models import Notification, Person, CaregiverLevel, Caregiver, SensorAlert, Home
from notifications_management.notification_level.notification_level_one import NotificationLevelOne
from notifications_management.notification_level.notification_level_three import NotificationLevelThree
from notifications_management.notification_level.notification_level_two import NotificationLevelTwo
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender
from ift785_project import settings
from notifications_management.notification_sender.notification_sender import NotificationSender


class EmailNotificationSenderTestCase(TestCase):
    def setUp(self):
        # Créer des objets nécessaires pour le test
        self.elderly = Person.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        self.caregiver = Person.objects.create(first_name="Jane", last_name="Doe", email="jane@example.com")
        self.caregiver_level = CaregiverLevel.objects.create(level=2)
        self.caregiver_instance = Caregiver.objects.create(elderly=self.elderly, caregiver=self.caregiver, level=self.caregiver_level)
        self.home = Home.objects.create(home="Test Home", elderly=self.elderly)
        self.sensor_alert = SensorAlert.objects.create(subject="Test Alert", start=datetime.now(), location="Test Location", state=0.5, measurable="Test Measurable", home=self.home)
        self.notification = Notification.objects.create(caregiver=self.caregiver_instance, sensor_alert=self.sensor_alert, token="test_token")

    def test_generate_subject_EmailNotificationSender_NotificationLevelOne(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

        # Appeler la méthode generate_subject avec la notification
        subject = email_sender.level.generate_subject(self.notification)

        # Vérifier si le sujet généré est correct
        expected_subject = f"Alert detected for {self.elderly.first_name} {self.elderly.last_name} ({self.sensor_alert.location})"
        self.assertEqual(subject, expected_subject)

    def test_generate_subject_EmailNotificationSender_NotificationLevelTwo(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

        # Appeler la méthode generate_subject avec la notification
        subject = email_sender.level.generate_subject(self.notification)

        # Vérifier si le sujet généré est correct
        expected_subject = f"REMINDER : Alert detected for {self.elderly.first_name} {self.elderly.last_name} ({self.sensor_alert.location})"
        self.assertEqual(subject, expected_subject)

    def test_generate_subject_EmailNotificationSender_NotificationLevelThree(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

        # Appeler la méthode generate_subject avec la notification
        subject = email_sender.level.generate_subject(self.notification)

        # Vérifier si le sujet généré est correct
        expected_subject = f"Assistance Requested for {self.elderly.first_name} {self.elderly.last_name} - Caregiver {self.caregiver_level}"
        self.assertEqual(subject, expected_subject)
