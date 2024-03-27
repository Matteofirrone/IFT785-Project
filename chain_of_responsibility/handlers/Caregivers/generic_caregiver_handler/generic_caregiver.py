from chain_of_responsibility.handlers.base_handler import BaseHandler


class GenericCaregiverHandler(BaseHandler):
    def handle(self, request):

        # It passes the request to the next handler if it can't handle it
        super().handle(request)