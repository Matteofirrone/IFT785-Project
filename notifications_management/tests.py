from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from api.models import Notification, Person, CaregiverLevel, Caregiver, SensorAlert, Home
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender
from ift785_project import settings

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

    def test_generate_subject(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender()

        # Appeler la méthode generate_subject avec la notification
        subject = email_sender.generate_subject(self.notification)

        # Vérifier si le sujet généré est correct
        expected_subject = f"Assistance Requested for {self.elderly.first_name} {self.elderly.last_name} - Caregiver Level {self.caregiver_level.level}"
        self.assertEqual(subject, expected_subject)

    def test_get_recipient(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender()

        # Appeler la méthode get_recipient avec la notification
        recipient = email_sender.get_recipient(self.notification)

        # Vérifier si le destinataire est correct
        expected_recipient = self.caregiver.email
        self.assertEqual(recipient, expected_recipient)

    def test_generate_content(self):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender()

        # Appelez la méthode generate_content avec la notification
        content = email_sender.generate_content(self.notification)

        # Vérifiez si le contenu contient les informations de la notification
        self.assertIn(self.elderly.first_name, content)
        self.assertIn(self.elderly.last_name, content)
        self.assertIn(str(self.caregiver_level.level), content)
        self.assertIn(str(self.sensor_alert.start), content)
        self.assertIn(self.sensor_alert.location, content)
        self.assertIn(str(self.sensor_alert.state), content)
        self.assertIn(self.sensor_alert.measurable, content)

    @patch('notifications_management.notification_sender.email_notification_sender.send_mail')
    def test_send(self, mock_send_mail):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender()

        # Paramètres de test
        subject = "Test Subject"
        content = "Test Content"
        recipient = "test@example.com"

        # Appelez la méthode send avec les paramètres de test
        email_sender.send(subject, content, recipient)

        # Vérifiez si send_mail a été appelé avec les bons arguments
        mock_send_mail.assert_called_once_with(
            subject=subject,
            message=content,
            from_email=settings.EMAIL_FROM,  # Utilisez le paramètre par défaut pour 'from_email'
            recipient_list=[recipient],
            fail_silently=False,
        )
