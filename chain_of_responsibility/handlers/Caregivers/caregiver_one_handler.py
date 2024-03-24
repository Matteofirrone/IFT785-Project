from chain_of_responsibility.handlers.base_handler import BaseHandler


class CaregiverOneHandler(BaseHandler):
    """
   Concrete handler class representing the first caregiver in the chain.

   Inherits from:
       BaseHandler

   Methods:
       handle(request): Handles the incoming request.
   """

    def handle(self, request):
        """
        Handle the incoming request. Passes the request to the next handler if available.

        Args:
            request: The request to be handled.
        """

        # Specific logic of CaregiverOneHandler

        # Passes the request to the next handler if available
        super().handle(request)
