from chain_of_responsibility.handlers.abstract_handler import Handler


class BaseHandler(Handler):
    """
    Base class implementing common functionality for handlers.

    Attributes:
        _next_handler: The next handler in the chain.
        _head_of_chain: The head of the chain.
    """
    _next_handler = None

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
