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

class CoursePermissionMiddleware(MiddlewareMixin):
    @permission_classes([IsAuthenticated])
    def process_request(self, request):
        assert hasattr(request, 'user'), "None"

        if request.user.is_authenticated:

            route = list(filter(None, request.path_info.split('/')))
            if route and len(route) > 1:
                base_route_name = route[0]
                route_name = route[1]
                if base_route_name == 'api' and route_name == 'courses' and len(route) > 2 and route[2].isdigit():
                    course_id = route[2]
                    filter_kwargs = {
                    'id': course_id
                    }
                    course, found, error = get_object(model=Course, filter_kwargs=filter_kwargs)
                    if not found:
                        return JsonResponse(error, status=404)
                    if not allowed_to_access_course(request.user, course):
                        return JsonResponse(general_utils.error('access_denied'), status=401)
