from unittest import mock

from django.test import TestCase

from api.models import Person, CaregiverLevel, Home, Caregiver, SensorAlert, Notification
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_one_handler import \
    CaregiverOneHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.generic_caregiver import \
    GenericCaregiverHandler


class GenericCaregiverHandlerTestCase(TestCase):
    def setUp(self):
        """
        This method creates the necessary instances for the tests and link them together
        (elderly person, caregiver, caregiver level, home, sensor alert).
        These instances will be used in the different tests.
        """
        self.elderly_person = Person.objects.create(first_name='John', last_name='Doe', email='john@example.com')
        self.caregiver_person = Person.objects.create(first_name='Jane', last_name='Doe', email='jane@example.com')
        self.caregiver_level = CaregiverLevel.objects.create(level=1)
        self.home = Home.objects.create(home='nears-hub-dev', elderly=self.elderly_person)
        self.caregiver = Caregiver.objects.create(elderly=self.elderly_person, caregiver=self.caregiver_person, level=self.caregiver_level)
        self.sensor_alert = SensorAlert.objects.create(subject='stove', start='2022-05-09T16:13:09.754Z', location='kitchen', state=29.22, measurable='anomalous_location_temperature', home=self.home)

    def test_build_notification(self):
        """
        This test verifies that the `build_notification` method of the `GenericCaregiverHandler` class
        correctly creates an instance of `Notification` with the right attributes
        (`caregiver`, `sensor_alert`, and `token`).
        """
        notification = GenericCaregiverHandler.build_notification(self.caregiver, self.sensor_alert)
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.caregiver, self.caregiver)
        self.assertEqual(notification.sensor_alert, self.sensor_alert)
        self.assertIsNotNone(notification.token)

    def test_generate_token(self):
        """
        This test verifies that the `generate_token` method of the `GenericCaregiverHandler` class
        generates a token of type string (`str`) and that this token does not already exist in the database.
        """
        token = GenericCaregiverHandler.generate_token()
        self.assertIsInstance(token, str)
        self.assertFalse(Notification.objects.filter(token=token).exists())

    @mock.patch('notifications_management.notification_sender.notification_sender.NotificationSender'
                '.deliver_notification')
    def test_handle(self, mock_deliver_notification):
        """
        This test verifies that the `handle` method of the `CaregiverOneHandler` class
        correctly calls the `deliver_notification` method of the `NotificationSender` class
        with a `Notification` instance containing the correct `caregiver` and `sensor_alert`.
        """
        handler = CaregiverOneHandler()
        handler.get_caregivers = mock.Mock(return_value=[self.caregiver])
        handler.handle(self.sensor_alert)

        self.assertTrue(mock_deliver_notification.called)
        notification = mock_deliver_notification.call_args[0][0]
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.caregiver, self.caregiver)
        self.assertEqual(notification.sensor_alert, self.sensor_alert)

    def test_timer_callback(self):
        """
        This test verifies that the `timer_callback` method of the `CaregiverOneHandler` class
        correctly calls the `handle` method of the next handler in the chain of responsibility
        with the same `sensor_alert`.
        """
        handler = CaregiverOneHandler()
        handler._next_handler = mock.Mock()
        handler.timer_callback(self.sensor_alert)
        handler._next_handler.handle.assert_called_once_with(self.sensor_alert)

    @mock.patch('notifications_management.notification_sender.notification_sender.NotificationSender'
                '.deliver_notification')
    def test_on_notification_accepted(self, mock_deliver_notification):
        """
        This test verifies that the `on_notification_accepted` method of the `CaregiverOneHandler` class
        correctly cancels the timer when a notification is accepted by a caregiver.
        """
        handler = CaregiverOneHandler()
        handler.get_caregivers = mock.Mock(return_value=[self.caregiver])
        handler.handle(self.sensor_alert)

        notification = mock_deliver_notification.call_args[0][0]
        handler._timer = mock.Mock()
        handler.on_notification_accepted(notification=notification)
        handler._timer.cancel.assert_called_once()
