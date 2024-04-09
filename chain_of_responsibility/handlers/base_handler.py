import uuid

from api.models import Notification, Caregiver, SensorAlert
from chain_of_responsibility.handlers.abstract_handler import Handler


class BaseHandler(Handler):
    """
    Base class implementing common functionality for handlers.

    Attributes:
        _next_handler: The next handler in the chain.
        _head_of_chain: The head of the chain.
    """
    _next_handler = None

    @staticmethod
    def build_notification(caregiver: Caregiver, sensor_alert: SensorAlert) -> Notification:
        """
        Builds a new notification for the given caregiver and sensor alert.

        :param caregiver: The association between an elderly_person and a caregiver.
        :param sensor_alert: The sensor alert that triggered the notification.
        :return: The new notification.
        """
        notification = Notification(caregiver=caregiver, sensor_alert=sensor_alert,
                                    token=BaseHandler.generate_token())
        notification.save()
        return notification

    @staticmethod
    def generate_token() -> str:
        """
        Generates a unique token for a notification.

        :return: A unique token.
        """
        token = str(uuid.uuid4())

        # Check if the UUID already exists
        while Notification.objects.filter(token=token).exists():
            token = str(uuid.uuid4())

        return token

    def __init__(self, head_of_chain=None):
        """
        Initializes a new instance of the `BaseHandler` class.

        Args:
            head_of_chain: The head of the chain.
        """
        self._next_handler = None
        if head_of_chain is None:
            self._head_of_chain = self
        else:
            self._head_of_chain = head_of_chain
        self._timer = None
        self._generated_notifications = set()

    def set_next(self, handler):
        """
        Set the next handler in the chain.

        Args:
            handler: The next handler to be set.

        Returns:
            Handler: The next handler.
        """
        self._next_handler = handler
        return handler

    def get_next(self):
        """
        Get the next handler in the chain.

        Returns:
            Handler: The next handler.
        """
        return self._next_handler

    def handle(self, request):
        """
        Passes the request to the next handler if available.

        Args:
            request: The request to be handled.
        """
        if self._next_handler:
            self._next_handler.handle(request)

    def remove_chain(self) -> None:
        """
        Removes the chain of responsibility from the list once it has completed its work.
        """
        from chain_of_responsibility.chain_manager import ChainManager
        chain_manager = ChainManager()
        chain_manager.remove_chain(self._head_of_chain)

    # Other comon methods to implement
