from datetime import datetime
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse

from api.models import Notification, Person, CaregiverLevel, Caregiver, SensorAlert, Home
from notifications_management.notification_level.notification_level import NotificationLevel
from notifications_management.notification_level.notification_level_one import NotificationLevelOne
from notifications_management.notification_level.notification_level_three import NotificationLevelThree
from notifications_management.notification_level.notification_level_two import NotificationLevelTwo
from notifications_management.notification_sender.email_notification_sender import EmailNotificationSender
from ift785_project import settings
from notifications_management.notification_sender.notification_sender import NotificationSender


class EmailNotificationSenderTestCase(TestCase):
    def setUp(self):
        # Create necessary objects for the test
        self.elderly = Person.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        self.caregiver = Person.objects.create(first_name="Jane", last_name="Doe", email="jane@example.com")
        self.caregiver_level = CaregiverLevel.objects.create(level=1)
        self.caregiver_instance = Caregiver.objects.create(elderly=self.elderly, caregiver=self.caregiver,
                                                           level=self.caregiver_level)
        self.home = Home.objects.create(home="Test Home", elderly=self.elderly)
        self.sensor_alert = SensorAlert.objects.create(subject="Test Alert", start=datetime.now(),
                                                       location="Test Location", state=0.5,
                                                       measurable="Test Measurable", home=self.home)
        self.notification = Notification.objects.create(caregiver=self.caregiver_instance,
                                                        sensor_alert=self.sensor_alert, token="test_token")

    def test_generate_subject_EmailNotificationSender_NotificationLevelOne(self):
        """
        Test the generate_subject method of EmailNotificationSender with NotificationLevelOne.

        This test verifies that the subject generated for NotificationLevelOne contains the correct information.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

        # Call generate_subject method with the notification
        subject = email_sender.level.generate_subject(self.notification)

        # Check if the generated subject is correct
        expected_subject = f"Alert detected for {self.elderly.first_name} {self.elderly.last_name} ({self.sensor_alert.location})"
        self.assertEqual(subject, expected_subject)

    def test_generate_subject_EmailNotificationSender_NotificationLevelTwo(self):
        """
        Test the generate_subject method of EmailNotificationSender with NotificationLevelTwo.

        This test verifies that the subject generated for NotificationLevelTwo contains the correct information.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

        # Call generate_subject method with the notification
        subject = email_sender.level.generate_subject(self.notification)

        # Check if the generated subject is correct
        expected_subject = f"REMINDER : Alert detected for {self.elderly.first_name} {self.elderly.last_name} ({self.sensor_alert.location})"
        self.assertEqual(subject, expected_subject)

    def test_generate_subject_EmailNotificationSender_NotificationLevelThree(self):
        """
        Test the generate_subject method of EmailNotificationSender with NotificationLevelThree.

        This test verifies that the subject generated for NotificationLevelThree contains the correct information.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

        # Call generate_subject method with the notification
        subject = email_sender.level.generate_subject(self.notification)

        # Check if the generated subject is correct
        expected_subject = f"Assistance Requested for {self.elderly.first_name} {self.elderly.last_name} - Caregiver {self.caregiver_level}"
        self.assertEqual(subject, expected_subject)

    def test_generate_subject_with_null_level(self):
        """
        Test the generate_subject method of EmailNotificationSender with a null level.

        This test verifies that an exception is raised when trying to generate a subject with a null level.
        """

        # Create an instance of NotificationSender with a dummy object for level
        sender = EmailNotificationSender(level=None)

        # Create an instance of Notification to test the generate_subject method
        notification = self.notification

        # Test if a ValueError exception is raised
        with self.assertRaises(ValueError):
            sender.generate_subject(notification)

    def test_get_recipient_EmailNotificationSender_NotificationLevelOne(self):
        """
        Test the get_recipient method of EmailNotificationSender with NotificationLevelOne.

        This test verifies that the recipient returned for NotificationLevelOne is correct.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

        # Call get_recipient method with the notification
        recipient = email_sender.get_recipient(self.notification)

        # Check if the recipient is correct
        expected_recipient = self.caregiver.email
        self.assertEqual(recipient, expected_recipient)

    def test_get_recipient_EmailNotificationSender_NotificationLevelTwo(self):
        """
        Test the get_recipient method of EmailNotificationSender with NotificationLevelTwo.

        This test verifies that the recipient returned for NotificationLevelTwo is correct.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

        # Call get_recipient method with the notification
        recipient = email_sender.get_recipient(self.notification)

        # Check if the recipient is correct
        expected_recipient = self.caregiver.email
        self.assertEqual(recipient, expected_recipient)

    def test_get_recipient_EmailNotificationSender_NotificationLevelThree(self):
        """
        Test the get_recipient method of EmailNotificationSender with NotificationLevelThree.

        This test verifies that the recipient returned for NotificationLevelThree is correct.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

        # Call get_recipient method with the notification
        recipient = email_sender.get_recipient(self.notification)

        # Check if the recipient is correct
        expected_recipient = self.caregiver.email
        self.assertEqual(recipient, expected_recipient)

    def test_generate_content_EmailNotificationSender_NotificationLevelOne(self):
        """
        Test the generate_content method of EmailNotificationSender with NotificationLevelOne.

        This test verifies that the content generated for NotificationLevelOne contains the correct information.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

        # Call generate_content method with the notification
        content = email_sender.generate_content(self.notification)

        # Check if the content contains the notification information
        self.assertIn(self.elderly.first_name, content)
        self.assertIn(self.elderly.last_name, content)
        self.assertIn(str(self.caregiver_level.level), content)
        self.assertIn(str(self.sensor_alert.start), content)
        self.assertIn(self.sensor_alert.location, content)
        self.assertIn(str(self.sensor_alert.state), content)
        self.assertIn(self.sensor_alert.measurable, content)
        self.assertIn(f"(This in an alert with level 1)", content)

    def test_generate_content_EmailNotificationSender_NotificationLevelTwo(self):
        """
        Test the generate_content method of EmailNotificationSender with NotificationLevelTwo.

        This test verifies that the content generated for NotificationLevelTwo contains the correct information.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

        # Call generate_content method with the notification
        content = email_sender.generate_content(self.notification)

        # Check if the content contains the notification information
        self.assertIn(self.elderly.first_name, content)
        self.assertIn(self.elderly.last_name, content)
        self.assertIn(str(self.caregiver_level.level), content)
        self.assertIn(str(self.sensor_alert.start), content)
        self.assertIn(self.sensor_alert.location, content)
        self.assertIn(str(self.sensor_alert.state), content)
        self.assertIn(self.sensor_alert.measurable, content)
        self.assertIn(f"(This in an alert with level 2)", content)

    def test_generate_content_EmailNotificationSender_NotificationLevelThree(self):
        """
        Test the generate_content method of EmailNotificationSender with NotificationLevelThree.

        This test verifies that the content generated for NotificationLevelThree contains the correct information.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

        # Call generate_content method with the notification
        content = email_sender.generate_content(self.notification)

        # Check if the content contains the notification information
        self.assertIn(self.elderly.first_name, content)
        self.assertIn(self.elderly.last_name, content)
        self.assertIn(str(self.caregiver_level.level), content)
        self.assertIn(str(self.sensor_alert.start), content)
        self.assertIn(self.sensor_alert.location, content)
        self.assertIn(str(self.sensor_alert.state), content)
        self.assertIn(self.sensor_alert.measurable, content)
        self.assertIn(f"(This in an alert with level 3)", content)

    def test_generate_content_with_level_None(self):
        """
        Test the generate_content method of EmailNotificationSender with a null level.

        This test verifies that an exception is raised when trying to generate content with a null level.
        """

        # Create an instance of NotificationSender with level=None
        sender = EmailNotificationSender(None)

        # Create an instance of Notification to test the generate_content method
        notification = MagicMock()

        # Test if a ValueError exception is raised
        with self.assertRaises(ValueError):
            sender.generate_content(notification)

    @patch('notifications_management.notification_sender.email_notification_sender.send_mail')
    def test_send_with_Strategy_NotificationLevelOne(self, mock_send_mail):
        """
        Test the send method of EmailNotificationSender with NotificationLevelOne.

        This test verifies that the email is sent correctly for NotificationLevelOne.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelOne())

        recipient = "test@example.com"

        # Call the send method with test parameters
        email_sender.send(email_sender.level.generate_subject(self.notification),
                          email_sender.level.generate_content(self.notification),
                          recipient)

        # Check if send_mail was called with the correct arguments
        mock_send_mail.assert_called_once_with(
            subject=email_sender.level.generate_subject(self.notification),
            message=email_sender.level.generate_content(self.notification),
            from_email=settings.EMAIL_FROM,  # Use the default parameter for 'from_email'
            recipient_list=[recipient],
            fail_silently=False,
        )

    @patch('notifications_management.notification_sender.email_notification_sender.send_mail')
    def test_send_with_Strategy_NotificationLevelTwo(self, mock_send_mail):
        """
        Test the send method of EmailNotificationSender with NotificationLevelTwo.

        This test verifies that the email is sent correctly for NotificationLevelTwo.
        """

        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelTwo())

        recipient = "test@example.com"

        # Call the send method with test parameters
        email_sender.send(email_sender.level.generate_subject(self.notification),
                          email_sender.level.generate_content(self.notification),
                          recipient)

        # Check if send_mail was called with the correct arguments
        mock_send_mail.assert_called_once_with(
            subject=email_sender.level.generate_subject(self.notification),
            message=email_sender.level.generate_content(self.notification),
            from_email=settings.EMAIL_FROM,  # Use the default parameter for 'from_email'
            recipient_list=[recipient],
            fail_silently=False,
        )

    @patch('notifications_management.notification_sender.email_notification_sender.send_mail')
    def test_send_with_Strategy_NotificationLevelThree(self, mock_send_mail):
        """
        Test the send method of EmailNotificationSender with NotificationLevelThree.

        This test verifies that the email is sent correctly for NotificationLevelThree.
        """
        # Create an instance of EmailNotificationSender
        email_sender = EmailNotificationSender(NotificationLevelThree())

        recipient = "test@example.com"

        # Call the send method with test parameters
        email_sender.send(email_sender.level.generate_subject(self.notification),
                          email_sender.level.generate_content(self.notification),
                          recipient)

        # Check if send_mail was called with the correct arguments
        mock_send_mail.assert_called_once_with(
            subject=email_sender.level.generate_subject(self.notification),
            message=email_sender.level.generate_content(self.notification),
            from_email=settings.EMAIL_FROM,  # Use the default parameter for 'from_email'
            recipient_list=[recipient],
            fail_silently=False,
        )


class NotificationSenderTestCase(TestCase):

    @patch('notifications_management.notification_sender.notification_sender.NotificationSender.send')
    def test_deliver_notification_Send_is_called_once(self, mock_send):
        """
        Test the deliver_notification method of NotificationSender.

        This test verifies that the send method is called with the correct arguments.
        """

        # Create an instance of NotificationSender (it's an abstract class, so we use a dummy subclass)
        class TestNotificationSender(NotificationSender):
            def generate_content(self, notification):
                return "Test Content"

            def generate_subject(self, notification):
                return "Test Subject"

            def get_recipient(self, notification):
                return "test@example.com"

        notification_sender = TestNotificationSender(NotificationLevelOne())

        # Create a notification object
        notification = Notification()

        # Call the deliver_notification method with the notification object
        notification_sender.deliver_notification(notification)

        # Check if the send method was called with the correct arguments
        mock_send.assert_called_once_with(subject="Test Subject", content="Test Content", recipient="test@example.com")

    @patch('notifications_management.notification_sender.notification_sender.reverse')
    def test_generate_link(self, mock_reverse):
        """
        Test the generate_link method of NotificationSender.

        This test verifies that the generated link contains the correct token.
        """

        # Test parameters
        notification = Notification()
        token = "test_token"
        notification.token = token
        domain = settings.DOMAIN
        expected_url = "/confirm_notification"  # Assume this is the expected URL for notification confirmation
        mock_reverse.return_value = expected_url

        # Call the generate_link method without passing a Notification object
        generated_link = NotificationSender.generate_link(notification)

        # Check if the generated URL is correct
        self.assertEqual(generated_link, f"{domain}{expected_url}?token={token}")

    """
    Tests methods: get_level & set_level
    """

    def test_level_setter(self):
        """
        Test the setter method for the level attribute of NotificationSender.

        This test verifies that the setter correctly assigns a new value for the level attribute.
        """

        # Create an instance of NotificationLevel to simulate a level value
        level = NotificationLevelOne()

        # Create an instance of NotificationSender
        sender = EmailNotificationSender(level=None)

        # Call the setter to set a new value for level
        sender.level = level

        # Check if the new value was correctly assigned
        self.assertEqual(sender.level, level)

    def test_level_getter(self):
        """
        Test the getter method for the level attribute of NotificationSender.

        This test verifies that the getter returns the correct value for the level attribute.
        """

        # Create an instance of NotificationLevel to simulate a level value
        level = NotificationLevelOne()

        # Create an instance of NotificationSender with a level value
        sender = EmailNotificationSender(level=level)

        # Get the value of level using the getter
        retrieved_level = sender.level

        # Check if the retrieved value is the same as the one previously set
        self.assertEqual(retrieved_level, level)
