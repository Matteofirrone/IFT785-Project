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

    def test_get_recipient_EmailNotificationSender_NotificationLevelOne(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

        # Appeler la méthode get_recipient avec la notification
        recipient = email_sender.get_recipient(self.notification)

        # Vérifier si le destinataire est correct
        expected_recipient = self.caregiver.email
        self.assertEqual(recipient, expected_recipient)

    def test_get_recipient_EmailNotificationSender_NotificationLevelTwo(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

        # Appeler la méthode get_recipient avec la notification
        recipient = email_sender.get_recipient(self.notification)

        # Vérifier si le destinataire est correct
        expected_recipient = self.caregiver.email
        self.assertEqual(recipient, expected_recipient)

    def test_get_recipient_EmailNotificationSender_NotificationLevelThree(self):
        # Créer une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

        # Appeler la méthode get_recipient avec la notification
        recipient = email_sender.get_recipient(self.notification)

        # Vérifier si le destinataire est correct
        expected_recipient = self.caregiver.email
        self.assertEqual(recipient, expected_recipient)

    def test_generate_content_EmailNotificationSender_NotificationLevelOne(self):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

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
        self.assertIn(f"(This in an alert with level 1)", content)

    def test_generate_content_EmailNotificationSender_NotificationLevelTwo(self):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

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
        self.assertIn(f"(This in an alert with level 2)", content)

    def test_generate_content_EmailNotificationSender_NotificationLevelThree(self):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

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
        self.assertIn(f"(This in an alert with level 3)", content)

    @patch('notifications_management.notification_sender.email_notification_sender.send_mail')
    def test_send_with_Strategy_NotificationLevelOne(self, mock_send_mail):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

        recipient = "test@example.com"

        # Appelez la méthode send avec les paramètres de test
        email_sender.send(email_sender.level.generate_subject(self.notification),
                          email_sender.level.generate_content(self.notification),
                          recipient)

        # Vérifiez si send_mail a été appelé avec les bons arguments
        mock_send_mail.assert_called_once_with(
            subject=email_sender.level.generate_subject(self.notification),
            message=email_sender.level.generate_content(self.notification),
            from_email=settings.EMAIL_FROM,  # Utilisez le paramètre par défaut pour 'from_email'
            recipient_list=[recipient],
            fail_silently=False,
        )

    @patch('notifications_management.notification_sender.email_notification_sender.send_mail')
    def test_send_with_Strategy_NotificationLevelTwo(self, mock_send_mail):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

        recipient = "test@example.com"

        # Appelez la méthode send avec les paramètres de test
        email_sender.send(email_sender.level.generate_subject(self.notification),
                          email_sender.level.generate_content(self.notification),
                          recipient)

        # Vérifiez si send_mail a été appelé avec les bons arguments
        mock_send_mail.assert_called_once_with(
            subject=email_sender.level.generate_subject(self.notification),
            message=email_sender.level.generate_content(self.notification),
            from_email=settings.EMAIL_FROM,  # Utilisez le paramètre par défaut pour 'from_email'
            recipient_list=[recipient],
            fail_silently=False,
        )

    @patch('notifications_management.notification_sender.email_notification_sender.send_mail')
    def test_send_with_Strategy_NotificationLevelThree(self, mock_send_mail):
        # Créez une instance de EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

        recipient = "test@example.com"

        # Appelez la méthode send avec les paramètres de test
        email_sender.send(email_sender.level.generate_subject(self.notification),
                          email_sender.level.generate_content(self.notification),
                          recipient)

        # Vérifiez si send_mail a été appelé avec les bons arguments
        mock_send_mail.assert_called_once_with(
            subject=email_sender.level.generate_subject(self.notification),
            message=email_sender.level.generate_content(self.notification),
            from_email=settings.EMAIL_FROM,  # Utilisez le paramètre par défaut pour 'from_email'
            recipient_list=[recipient],
            fail_silently=False,
        )



class NotificationSenderTestCase(TestCase):

    @patch('notifications_management.notification_sender.notification_sender.NotificationSender.send')
    def test_deliver_notification_Send_is_called_once(self, mock_send):
        # Créez une instance de NotificationSender (c'est une classe abstraite, donc nous utilisons une sous-classe fictive)
        class TestNotificationSender(NotificationSender):
            def generate_content(self, notification):
                return "Test Content"

            def generate_subject(self, notification):
                return "Test Subject"

            def get_recipient(self, notification):
                return "test@example.com"

        notification_sender = TestNotificationSender(NotificationLevelOne())

        # Créez un objet de notification
        notification = Notification()

        # Appelez la méthode deliver_notification avec l'objet de notification
        notification_sender.deliver_notification(notification)

        # Vérifiez si la méthode send a été appelée avec les bons arguments
        mock_send.assert_called_once_with(subject="Test Subject", content="Test Content", recipient="test@example.com")

    @patch('notifications_management.notification_sender.notification_sender.reverse')
    def test_generate_link(self, mock_reverse):
        # Paramètres de test
        notification = Notification()
        token = "test_token"
        notification.token = token
        domain = settings.DOMAIN
        expected_url = "/confirm_notification"  # Supposons que c'est l'URL attendue pour la confirmation de notification
        mock_reverse.return_value = expected_url

        # Appelez la méthode generate_link sans passer d'objet Notification
        generated_link = NotificationSender.generate_link(notification)

        # Vérifiez si l'URL générée est correcte
        self.assertEqual(generated_link, f"{domain}{expected_url}?token={token}")