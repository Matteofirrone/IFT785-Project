from unittest import mock
from unittest.mock import patch, MagicMock
from django.test import TestCase

import api
from api.models import Person, CaregiverLevel, Home, Caregiver, SensorAlert, Notification
from chain_of_responsibility.chain_manager import ChainManager
from chain_of_responsibility.handlers.Caregivers.caregiver_zero_handler import CaregiverZeroHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_one_handler import \
    CaregiverOneHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_three_handler import \
    CaregiverThreeHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_two_handler import \
    CaregiverTwoHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.generic_caregiver import \
    GenericCaregiverHandler
from chain_of_responsibility.handlers.abstract_handler import Handler
from chain_of_responsibility.handlers.base_handler import BaseHandler
from notifications_management.notification_level.notification_level_one import NotificationLevelOne
from notifications_management.notification_level.notification_level_two import NotificationLevelTwo


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
        self.caregiver = Caregiver.objects.create(elderly=self.elderly_person, caregiver=self.caregiver_person,
                                                  level=self.caregiver_level)
        self.sensor_alert = SensorAlert.objects.create(subject='stove', start='2022-05-09T16:13:09.754Z',
                                                       location='kitchen', state=29.22,
                                                       measurable='anomalous_location_temperature', home=self.home)

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

        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        handler = CaregiverOneHandler(head_of_chain)
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

        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        handler = CaregiverOneHandler(head_of_chain)
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

        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        handler = CaregiverOneHandler(head_of_chain)
        handler.get_caregivers = mock.Mock(return_value=[self.caregiver])
        handler.handle(self.sensor_alert)

        notification = mock_deliver_notification.call_args[0][0]
        handler._timer = mock.Mock()
        handler.on_notification_accepted(notification=notification)
        handler._timer.cancel.assert_called_once()


class ChainManagerTestCase(TestCase):
    """
    Test case class for ChainManager.
    """

    def setUp(self):
        self.caregiver_level = CaregiverLevel.objects.create(level=0)
        self.caregiver_level = CaregiverLevel.objects.create(level=1)
        self.caregiver_level = CaregiverLevel.objects.create(level=2)
        self.caregiver_level = CaregiverLevel.objects.create(level=3)

    def test_singleton(self):
        """
        Test the singleton behavior of the ChainManager class.
        This test verifies that only one instance of ChainManager can be created.
        """
        # Create two instances of ChainManager
        manager1 = ChainManager()
        manager2 = ChainManager()

        # They should be the same instance
        self.assertIs(manager1, manager2)

    def test_initialize_chain_of_responsibility(self):
        """
        Test the initialize_chain_of_responsibility method of the ChainManager class.
        This test verifies that the method correctly initializes a new chain of responsibility.
        """
        # Get the ChainManager instance
        manager = ChainManager()

        # Initialize a new chain of responsibility
        chain = manager.initialize_chain_of_responsibility()

        # It should be an instance of Handler
        self.assertIsInstance(chain, Handler)

    def test_get_chain_of_responsibility(self):
        """
        Test the get_chain_of_responsibility method of the ChainManager class.
        This test ensures that a new chain of responsibility can be correctly retrieved.
        """
        # Get the ChainManager instance
        manager = ChainManager()

        # Get two chains of responsibility
        chain1 = manager.get_chain_of_responsibility()
        chain2 = manager.get_chain_of_responsibility()

        # They should be different instances of Handler
        self.assertIsInstance(chain1, Handler)
        self.assertIsInstance(chain2, Handler)
        self.assertIsNot(chain1, chain2)

    def test_get_chains_of_responsibility(self):
        """
        Test the get_chains_of_responsibility method of the ChainManager class.
        This test ensures that all chains of responsibility can be correctly retrieved.
        """
        # Get the ChainManager instance
        manager = ChainManager()

        # Initialize two chains of responsibility
        chain1 = manager.initialize_chain_of_responsibility()
        chain2 = manager.initialize_chain_of_responsibility()

        # Get the list of chains of responsibility
        chains = manager.get_chains_of_responsibility()

        # It should contain the two chains
        self.assertIn(chain1, chains)
        self.assertIn(chain2, chains)

    def test_remove_chain(self):
        """
        Test the remove_chain method of the ChainManager class.
        This test ensures that a chain of responsibility can be correctly removed.
        """
        # Get the ChainManager instance
        manager = ChainManager()

        # Initialize two chains of responsibility
        chain1 = manager.initialize_chain_of_responsibility()
        chain2 = manager.initialize_chain_of_responsibility()

        # Remove the first chain
        manager.remove_chain(chain1)

        # The list of chains should only contain the second chain
        chains = manager.get_chains_of_responsibility()
        self.assertIn(chain2, chains)
        self.assertNotIn(chain1, chains)


class HandlersTestCase(TestCase):
    def setUp(self):
        """
        This method creates the necessary instances for the tests and link them together
        (elderly person, caregiver, caregiver level, home, sensor alert).
        These instances will be used in the different tests.
        """
        self.elderly_person = Person.objects.create(first_name='John', last_name='Doe', email='john@example.com')
        self.caregiver_person_one = Person.objects.create(first_name='Jane', last_name='Doe', email='jane@example.com')
        self.caregiver_person_one_2 = Person.objects.create(first_name='Janette', last_name='Philips',
                                                            email='janette@example.com')
        self.caregiver_person_two = Person.objects.create(first_name='Sam', last_name='Smith', email='sam@example.com')
        self.caregiver_person_two_2 = Person.objects.create(first_name='Sammy', last_name='Johnson',
                                                            email='sammy@example.com')
        self.caregiver_person_three = Person.objects.create(first_name='Felix', last_name='Williams',
                                                            email='felix@example.com')
        self.caregiver_person_three_2 = Person.objects.create(first_name='Josh', last_name='Williamson',
                                                              email='josh@example.com')
        self.caregiver_level_one = CaregiverLevel.objects.create(level=1)
        self.caregiver_level_two = CaregiverLevel.objects.create(level=2)
        self.caregiver_level_three = CaregiverLevel.objects.create(level=3)
        self.caregiver_level_zero = CaregiverLevel.objects.create(level=0)
        self.home = Home.objects.create(home='nears-hub-dev', elderly=self.elderly_person)
        self.caregiverLevelOne = Caregiver.objects.create(elderly=self.elderly_person,
                                                          caregiver=self.caregiver_person_one,
                                                          level=self.caregiver_level_one)
        self.caregiverLevelOne_2 = Caregiver.objects.create(elderly=self.elderly_person,
                                                            caregiver=self.caregiver_person_one_2,
                                                            level=self.caregiver_level_one)
        self.caregiverLevelTwo = Caregiver.objects.create(elderly=self.elderly_person,
                                                          caregiver=self.caregiver_person_two,
                                                          level=self.caregiver_level_two)
        self.caregiverLevelTwo_2 = Caregiver.objects.create(elderly=self.elderly_person,
                                                            caregiver=self.caregiver_person_two_2,
                                                            level=self.caregiver_level_two)
        self.caregiverLevelThree = Caregiver.objects.create(elderly=self.elderly_person,
                                                            caregiver=self.caregiver_person_three,
                                                            level=self.caregiver_level_three)
        self.caregiverLevelThree_2 = Caregiver.objects.create(elderly=self.elderly_person,
                                                              caregiver=self.caregiver_person_three_2,
                                                              level=self.caregiver_level_three)
        self.caregiverLevelZero = Caregiver.objects.create(elderly=self.elderly_person, caregiver=self.elderly_person,
                                                           level=self.caregiver_level_zero)
        self.sensor_alert = SensorAlert.objects.create(subject='stove', start='2022-05-09T16:13:09.754Z',
                                                       location='kitchen', state=29.22,
                                                       measurable='anomalous_location_temperature', home=self.home)

    def test_getCaregivers_CaregiverZeroHandler(self):
        """
            Test the get_caregivers method of the CaregiverZeroHandler class.
            This test ensures that the caregiver returning by the method is at the good level (0)
        """
        # Creating an instance of the CaregiverZeroHandler handler
        handler = CaregiverZeroHandler()

        caregiver = handler.get_caregiver(self.sensor_alert)

        # Checking that the handler returns the correct level zero caregiver for the sensor alert
        self.assertEqual(self.caregiverLevelZero, caregiver)

        # Checking that the handler does not return higher level caregivers for the sensor alert
        self.assertNotEqual(self.caregiverLevelOne, caregiver)
        self.assertNotEqual(self.caregiverLevelTwo, caregiver)
        self.assertNotEqual(self.caregiverLevelThree, caregiver)

        # Check that the caregiver returned are associated with the elderly person
        self.assertEqual(caregiver.elderly, self.elderly_person)

    def test_getCaregivers_CaregiverOneHandler(self):
        """
            Test the get_caregivers method of the CaregiverOneHandler class.
            This test ensures that the caregiver returning by the method is at the good level (1)
        """
        # Create a mock head of the chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        # Create an instance of the CaregiverOneHandler with the mock head of the chain
        handler = CaregiverOneHandler(head_of_chain)

        # Get the caregivers returned by the handler for the sensor alert
        caregivers = handler.get_caregivers(self.sensor_alert)

        # Check that the handler returns level one caregivers for the sensor alert
        self.assertIn(self.caregiverLevelOne, caregivers)

        # Check that the handler does not return caregivers of other levels for the sensor alert
        self.assertNotIn(self.caregiverLevelZero, caregivers)
        self.assertNotIn(self.caregiverLevelTwo, caregivers)
        self.assertNotIn(self.caregiverLevelThree, caregivers)

        # Check that all caregivers returned are associated with the elderly person
        for caregiver in caregivers:
            self.assertEqual(caregiver.elderly, self.elderly_person)

    def test_getCaregivers_CaregiverTwoHandler(self):
        """
            Test the get_caregivers method of the CaregiverTwoHandler class.
            This test ensures that the caregiver returning by the method is at the good level (2)
        """
        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        # Create an instance of the CaregiverTwoHandler with the mock head of the chain
        handler = CaregiverTwoHandler(head_of_chain)

        # Get the caregivers returned by the handler for the sensor alert
        caregivers = handler.get_caregivers(self.sensor_alert)

        # Check that the handler returns level two caregivers for the sensor alert
        self.assertIn(self.caregiverLevelTwo, caregivers)

        # Check that the handler does not return caregivers of other levels for the sensor alert
        self.assertNotIn(self.caregiverLevelZero, caregivers)
        self.assertNotIn(self.caregiverLevelOne, caregivers)
        self.assertNotIn(self.caregiverLevelThree, caregivers)

        # Check that all caregivers returned are associated with the elderly person
        for caregiver in caregivers:
            self.assertEqual(caregiver.elderly, self.elderly_person)

    def test_getCaregivers_CaregiverThreeHandler(self):
        """
            Test the get_caregivers method of the CaregiverThreeHandler class.
            This test ensures that the caregiver returning by the method is at the good level (3)
        """
        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        # Create an instance of the CaregiverThreeHandler with the mock head of the chain
        handler = CaregiverThreeHandler(head_of_chain)

        # Get the caregivers returned by the handler for the sensor alert
        caregivers = handler.get_caregivers(self.sensor_alert)

        # Check that the handler returns level three caregivers for the sensor alert
        self.assertIn(self.caregiverLevelThree, caregivers)

        # Check that the handler does not return caregivers of other levels for the sensor alert
        self.assertNotIn(self.caregiverLevelZero, caregivers)
        self.assertNotIn(self.caregiverLevelOne, caregivers)
        self.assertNotIn(self.caregiverLevelTwo, caregivers)

        # Check that all caregivers returned are associated with the elderly person
        for caregiver in caregivers:
            self.assertEqual(caregiver.elderly, self.elderly_person)

    def test_getCaregivers_MultipleCaregiversLevelOne(self):
        """
            Test the get_caregivers method of the CaregiverThreeHandler class.
            This test ensures that the caregivers returning by the method is at the good level (1)
        """
        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        # Create an instance of the CaregiverThreeHandler with the mock head of the chain
        handler = CaregiverOneHandler(head_of_chain)

        # Get the caregivers returned by the handler for the sensor alert
        caregivers = handler.get_caregivers(self.sensor_alert)

        # Check that the handler returns level three caregivers for the sensor alert
        self.assertIn(self.caregiverLevelOne, caregivers)
        self.assertIn(self.caregiverLevelOne_2, caregivers)

        # Check that the handler does not return caregivers of other levels for the sensor alert
        self.assertNotIn(self.caregiverLevelZero, caregivers)
        self.assertNotIn(self.caregiverLevelTwo, caregivers)
        self.assertNotIn(self.caregiverLevelTwo_2, caregivers)
        self.assertNotIn(self.caregiverLevelThree, caregivers)
        self.assertNotIn(self.caregiverLevelThree_2, caregivers)

        # Check that all caregivers returned are associated with the elderly person
        for caregiver in caregivers:
            self.assertEqual(caregiver.elderly, self.elderly_person)

    def test_getCaregivers_MultipleCaregiversLevelTwo(self):
        """
            Test the get_caregivers method of the CaregiverThreeHandler class.
            This test ensures that the caregivers returning by the method is at the good level (2)
        """
        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        # Create an instance of the CaregiverThreeHandler with the mock head of the chain
        handler = CaregiverTwoHandler(head_of_chain)

        # Get the caregivers returned by the handler for the sensor alert
        caregivers = handler.get_caregivers(self.sensor_alert)

        # Check that the handler returns level three caregivers for the sensor alert
        self.assertIn(self.caregiverLevelTwo, caregivers)
        self.assertIn(self.caregiverLevelTwo_2, caregivers)

        # Check that the handler does not return caregivers of other levels for the sensor alert
        self.assertNotIn(self.caregiverLevelZero, caregivers)
        self.assertNotIn(self.caregiverLevelOne, caregivers)
        self.assertNotIn(self.caregiverLevelOne_2, caregivers)
        self.assertNotIn(self.caregiverLevelThree, caregivers)
        self.assertNotIn(self.caregiverLevelThree_2, caregivers)

        # Check that all caregivers returned are associated with the elderly person
        for caregiver in caregivers:
            self.assertEqual(caregiver.elderly, self.elderly_person)

    def test_getCaregivers_MultipleCaregiversLevelThree(self):
        """
            Test the get_caregivers method of the CaregiverThreeHandler class.
            This test ensures that the caregivers returning by the method is at the good level (3)
        """
        # Create a mock head of chain
        head_of_chain = mock.Mock(spec=BaseHandler)

        # Create an instance of the CaregiverThreeHandler with the mock head of the chain
        handler = CaregiverThreeHandler(head_of_chain)

        # Get the caregivers returned by the handler for the sensor alert
        caregivers = handler.get_caregivers(self.sensor_alert)

        # Check that the handler returns level three caregivers for the sensor alert
        self.assertIn(self.caregiverLevelThree, caregivers)
        self.assertIn(self.caregiverLevelThree_2, caregivers)

        # Check that the handler does not return caregivers of other levels for the sensor alert
        self.assertNotIn(self.caregiverLevelZero, caregivers)
        self.assertNotIn(self.caregiverLevelOne, caregivers)
        self.assertNotIn(self.caregiverLevelOne_2, caregivers)
        self.assertNotIn(self.caregiverLevelTwo, caregivers)
        self.assertNotIn(self.caregiverLevelTwo_2, caregivers)

        # Check that all caregivers returned are associated with the elderly person
        for caregiver in caregivers:
            self.assertEqual(caregiver.elderly, self.elderly_person)


class CaregiverZeroHandlerTest(TestCase):
    """
        This class contains test cases for the CaregiverZeroHandler class.
    """
    def setUp(self):
        """
        This method sets up the necessary objects for the tests.
        It creates an elderly person, a home, a sensor alert, and a caregiver level zero.
        """
        self.elderly = Person.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com')
        self.home = Home.objects.create(home='nears-hub-dev', elderly=self.elderly)
        self.sensor_alert = SensorAlert.objects.create(subject='stove', start='2022-05-09T16:13:09.754Z',
                                                       location='kitchen', state=29.22,
                                                       measurable='anomalous_location_temperature', home=self.home)

        self.caregiver_level_zero = CaregiverLevel.objects.create(level=0, wait_time= 5)

    @patch('chain_of_responsibility.handlers.Caregivers.caregiver_zero_handler.EmailNotificationSender')
    def test_handles_request_with_existing_caregiver(self, mock_sender):
        """
        This test case checks if the handle method of the CaregiverZeroHandler class correctly sends a notification
        when there is an existing caregiver.
        """
        # Setup
        caregiverLevelZero = Caregiver.objects.create(elderly=self.elderly, caregiver=self.elderly,
                                                      level=self.caregiver_level_zero)
        request = self.sensor_alert
        handler = CaregiverZeroHandler()

        # Act
        handler.handle(request)

        # Assert
        call_args = mock_sender.call_args
        self.assertIsInstance(call_args[0][0], NotificationLevelOne)
        mock_sender.return_value.deliver_notification.assert_called()


    @patch('chain_of_responsibility.handlers.Caregivers.caregiver_zero_handler.EmailNotificationSender')
    def test_passes_request_to_next_handler_when_no_caregiver(self, mock_sender):
        """
        This test case checks if the handle method of the CaregiverZeroHandler class correctly passes the request
        to the next handler when there is no caregiver.
        """
        # Setup
        request = self.sensor_alert
        handler = CaregiverZeroHandler()

        # Act & Assert
        with self.assertRaises(api.models.Caregiver.DoesNotExist):
            handler.handle(request)

        mock_sender.assert_not_called()
    @patch('chain_of_responsibility.handlers.Caregivers.caregiver_zero_handler.EmailNotificationSender')
    def test_sends_second_notification_after_wait_time(self, mock_sender):
        """
        This test case checks if the handle method of the CaregiverZeroHandler class correctly sends a second notification
        after the wait time.
        """
        # Setup
        caregiver = Caregiver.objects.create(elderly=self.elderly, caregiver=self.elderly, level=self.caregiver_level_zero)
        request = self.sensor_alert
        handler = CaregiverZeroHandler()

        # Act
        handler.handle(request)
        handler._timer.join()

        # Assert
        call_args = mock_sender.call_args
        self.assertIsInstance(call_args[0][0], NotificationLevelTwo)
        mock_sender.return_value.deliver_notification.assert_called()

    @patch('chain_of_responsibility.handlers.Caregivers.caregiver_zero_handler.EmailNotificationSender')
    def test_passes_request_to_next_handler_after_second_wait_time(self, mock_sender):
        """
        This test case checks if the handle method of the CaregiverZeroHandler class correctly passes the request
        to the next handler after the second wait time.
        """
        # Setup
        caregiver = Caregiver.objects.create(elderly=self.elderly, caregiver=self.elderly, level=self.caregiver_level_zero)
        request = self.sensor_alert
        handler = CaregiverZeroHandler()
        handler.set_next(CaregiverZeroHandler())

        # Act
        handler.handle(request)
        handler._timer.join()
        handler._timer.join()

        # Assert
        call_args = mock_sender.call_args
        self.assertIsInstance(call_args[0][0], NotificationLevelTwo)
        mock_sender.return_value.deliver_notification.assert_called()
