from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve, reverse
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings by setting a tuple of routes to ignore
    """
    @permission_classes([IsAuthenticated])
    def process_request(self, request):
        assert hasattr(request, 'user'), """
        The Login Required middleware needs to be after AuthenticationMiddleware.
        Also make sure to include the template context_processor:
        'django.contrib.auth.context_processors.auth'."""

        if not request.user.is_authenticated:
            route = list(filter(None, request.path_info.split('/')))
            base_route_name = route[0]
            last_route_name = route[-1]
            if base_route_name in settings.AUTH_EXEMPT_ROUTES and last_route_name not in settings.ALLOWED_ENDPOINTS:
                return JsonResponse({
                'status': 'error',
                'error_description': 'Not Authenticated!'
                })
