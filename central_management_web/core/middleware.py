from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that don't require login
        self.exempt_urls = [reverse('core:login')]

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self.exempt_urls and not request.path_info.startswith('/static/'):
            return redirect('core:login')

        response = self.get_response(request)
        return response