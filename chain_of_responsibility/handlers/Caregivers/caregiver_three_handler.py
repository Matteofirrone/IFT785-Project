from chain_of_responsibility.handlers.base_handler import BaseHandler


class CaregiverThreeHandler(BaseHandler):
    def handle(self, request):
        # CaregiverZeroHandler logic here

        # It passes the request to the next handler if it can't handle it
        super().handle(request)
