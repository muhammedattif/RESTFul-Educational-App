import datetime
from django.db.models import Subquery, IntegerField

class SQCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = IntegerField()


def error(error_key):
    return {
        'status': False,
        'message': 'error',
        'error_description': error_messages[error_key]
    }

def success(success_key):
    return {
        'status': True,
        'message': 'success',
        'success_description': success_messages[success_key]
    }

def seconds_to_duration(seconds):
    if not seconds:
        seconds = 0
    duration = str(datetime.timedelta(seconds=seconds))
    duration_slices = duration.split(':')
    return f'{duration_slices[0]}h {duration_slices[1]}m {duration_slices[2]}s'


error_messages = {
    'internal_error': 'Internal Server Error.',
    'not_found': 'Not Found!',
    'access_denied': 'You don\'t have access to this resourse!, enroll this course to see its content.',
    'required_fields': 'Some fields are required.',
    'page_access_denied': 'You don\'t have access to preview this page.',
    'empty_quiz_answers': "Quiz answers cannot be empty."
}

success_messages = {
    'quiz_answer_submitted': "Quiz answers has been recorded.",
    'enrolled': "Course Successfully Enrolled!"
}
