from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Abstract base class for defining handlers in the chain of responsibility pattern.
    """

    @abstractmethod
    def set_next(self, handler):
        """
        Set the next handler in the chain.

        Args:
            handler: The next handler to be set.

        Returns:
            Handler: The next handler for chaining.
        """
        pass

    @abstractmethod
    def handle(self, request):
        """
        Handle the incoming request.

        Args:
            request: The request to be handled.
        """
        pass

