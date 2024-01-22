from django.conf import settings
from datetime import timedelta, date

class KeepLoggedInMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code for processing requests
        response = self.get_response(request)
        return response
    def process_request(self, request):
        if not request.user.is_authenticated() or not settings.KEEP_LOGGED_KEY in request.session:
            return
        if request.session[settings.KEEP_LOGGED_KEY] != date.today():
            request.session.set_expiry(timedelta(days=settings.KEEP_LOGGED_DURATION))
            request.session[settings.KEEP_LOGGED_KEY] = date.today()
        return