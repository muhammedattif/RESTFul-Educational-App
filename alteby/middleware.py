from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve, reverse
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from courses.models import Course
from courses.utils import get_object
from courses.utils import allowed_to_access_course, get_object
import alteby.utils as general_utils
from django.conf import settings
from re import sub
from rest_framework.authtoken.models import Token

class CoursePermissionMiddleware(MiddlewareMixin):

    @permission_classes([IsAuthenticated])
    def process_request(self, request):
        assert hasattr(request, 'user'), "None"

        self.route = list(filter(None, request.path_info.split('/')))
        self.route_len = len(self.route)

        if self.route and self.route_len > 2:
            self.base_route_name = self.route[0]
            self.route_name = self.route[1]
            self.course_id = self.route[2]
        else:
            return None

        if self.is_index_requested():
            return None


        if self.base_route_name == settings.BASE_PROTECTED_ROUTE and self.route_name == settings.PROTECTED_ROUTE and self.course_id.isdigit():

            header_token = request.META.get('HTTP_AUTHORIZATION', None)
            if header_token is not None:
              try:
                token = sub('Token ', '', request.META.get('HTTP_AUTHORIZATION', None))
                token_obj = Token.objects.get(key = token)
                request.user = token_obj.user
              except Token.DoesNotExist:
                return JsonResponse(general_utils.error('page_access_denied'), status=401)

            filter_kwargs = {
            'id': self.course_id
            }
            course, found, error = get_object(model=Course, filter_kwargs=filter_kwargs)
            if not found:
                return JsonResponse(error, status=404)
            if not allowed_to_access_course(request.user, course):
                return JsonResponse(general_utils.error('access_denied'), status=403)

    def is_index_requested(self):

        if not len(self.route) > 3:
            return False

        index_route = self.route[3]
        if index_route not in settings.ALLOWED_COURSE_ROUTES:
            return False
        return True
