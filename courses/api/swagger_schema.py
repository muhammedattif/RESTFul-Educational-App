from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import alteby.utils as general_utils

from .serializers import CourseSerializer


course_detail_response = {
    200: openapi.Response('Success Response', CourseSerializer),
    404: openapi.Response('Not Found Response', examples={"application/json": {
                'status': False,
                'message': 'error',
                'error_description': general_utils.error_messages['not_found']
            }}),
    403: openapi.Response('Access Denied Response', examples={"application/json": {
                'status': False,
                'message': 'error',
                'error_description': general_utils.error_messages['access_denied']
            }}),
}

course_detail_swagger_schema = swagger_auto_schema(operation_description="Course Details", responses=course_detail_response)
