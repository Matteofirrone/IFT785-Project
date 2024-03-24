from chain_of_responsibility.handlers.abstract_handler import Handler


class BaseHandler(Handler):
    """
    Base class implementing common functionality for handlers.

    Attributes:
        _next_handler: The next handler in the chain.
    """
    _next_handler = None

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

    def handle(self, request):
        """
        Passes the request to the next handler if available.

        Args:
            request: The request to be handled.
        """
        if self._next_handler:
            self._next_handler.handle(request)

    # Other comon methods to implement
    def send_email(self):
        """
        Placeholder for sending email logic. To be implemented in subclasses.
        """
        pass
