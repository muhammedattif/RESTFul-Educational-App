from django.http import JsonResponse
import alteby.utils as general_utils
from rest_framework.views import exception_handler


def custom_error_404(request, exception=None):
    error = general_utils.error('not_found')
    return JsonResponse(error, status=404)

def custom_error_500(request, exception=None):
    error = general_utils.error('internal_error')
    return JsonResponse(error, status=500)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
