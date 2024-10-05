from django.shortcuts import redirect
from django.urls import reverse

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            # Redirect admin users to the admin site
            if not request.path.startswith(reverse('admin:index')):
                return redirect('admin:index')
        response = self.get_response(request)
        return response