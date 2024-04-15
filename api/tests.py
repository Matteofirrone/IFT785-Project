from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIRequestFactory
from api.models import SensorAlert, Person, Home, Caregiver, Notification, CaregiverLevel
from api.views import SensorAlertView
from ift785_project import settings


class SensorAlertViewTestCase(TestCase):
    """
    This class is a Django TestCase for the SensorAlertView. It contains methods to set up test data and test the
    behavior of the SensorAlertView when receiving POST requests with valid and invalid data.
    """

    @classmethod
    def setUpTestData(cls):
        """
        This method is called once to set up non-modified data for all class methods. Here, it creates a Person and a
        Home object that will be used in the tests.
        """

        elderly = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )

        Home.objects.create(
            home='nears-hub-dev',
            elderly=elderly
        )

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SensorAlertView.as_view()

    @patch('api.views.throw_in_chain')
    def test_post_valid_data(self, mock_throw_in_chain):
        """
        This method tests the behavior of the SensorAlertView when it receives a POST request with valid data. It
        checks if the response status code is HTTP_200_OK, if the sensor alert was saved in the database, and if the
        throw_in_chain function was called with the correct arguments.
        """
        data = {
            "subject": "stove",
            "start": "2022-05-09T16:13:09.754Z",
            "location": "kitchen",
            "state": "29.22",
            "measurable": "anomalous_location_temperature",
            "home": "nears-hub-dev"
        }
        request = self.factory.post('/api/sensor-alerts/', data, format='json')
        response = self.view(request)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, HTTP_200_OK)

        # Check that the sensor alert was saved in the database
        self.assertTrue(SensorAlert.objects.filter(home__home=data['home']).exists())

        # Check that throw_in_chain was called with the correct arguments
        mock_throw_in_chain.assert_called_once_with(SensorAlert.objects.get(home__home=data['home']))

    @patch('api.views.throw_in_chain')
    def test_post_invalid_data(self, mock_throw_in_chain):
        """
        This method tests the behavior of the SensorAlertView when it receives a POST request with invalid data. It
        checks if the response status code is HTTP_400_BAD_REQUEST and if the throw_in_chain function was not called.
        """
        data = {
            "subject": "stove",
            "start": "2022-05-09T16:13:09.754Z",
            "location": "kitchen",
            "state": "29.22",
            "measurable": "anomalous_location_temperature",
            "home": "invalid-home"
        }
        request = self.factory.post('/api/sensor-alerts/', data, format='json')
        response = self.view(request)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Check that throw_in_chain was called with the correct arguments
        mock_throw_in_chain.assert_not_called()


class ConfirmNotificationViewTestCase(TestCase):
    """
    Django TestCase for the confirm_notification function. It contains methods to set up test data and test the
    behavior of the confirm_notification function when receiving GET requests with valid and invalid tokens.
    """
    @classmethod
    def setUpTestData(cls):
        """
        This method is called once to set up non-modified data for all class methods. Here, it creates a Person,
        Home, CaregiverLevel, Caregiver, SensorAlert, and Notification object that will be used in the tests.
        """
        elderly = Person.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com')
        home = Home.objects.create(home='nears-hub-dev', elderly=elderly)
        person = Person.objects.create(first_name='Mattéo', last_name='Firrone', email='firrone.matteo@example.com')
        caregiver_level = CaregiverLevel.objects.create(level=1)
        caregiver = Caregiver.objects.create(elderly=elderly, caregiver=person, level=caregiver_level)
        sensor_alert = SensorAlert.objects.create(subject='stove', start='2022-05-09T16:13:09.754Z', location='kitchen', state='29.22', measurable='anomalous_location_temperature', home=home)
        cls.notification = Notification.objects.create(token='12345', caregiver=caregiver, sensor_alert=sensor_alert)

    def test_confirm_notification_with_valid_token(self):
        """
        This method tests the behavior of the confirm_notification function when it receives a GET request with a
        valid token. It checks if the response status code is HTTP_200_OK.
        """
        # Call the view
        url = reverse('api:confirm_notification')
        domain = settings.DOMAIN
        response = self.client.get(f"{domain}{url}?token={12345}")

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_confirm_notification_with_invalid_token(self):
        """
        This method tests the behavior of the confirm_notification function when it receives a GET request with an
        invalid token. It checks if the response status code is HTTP_404_NOT_FOUND.
        """

        # Call the view
        url = reverse('api:confirm_notification')
        domain = settings.DOMAIN
        response = self.client.get(f"{domain}{url}?token={1234}")

        # Check that the response is 404_NOT_FOUND
        self.assertEqual(response.status_code, 404)
