from .models import Content, Course

def get_course(course_id):
    try:
        return Course.objects.get(id=course_id), True, None
    except Course.DoesNotExist:
        error = {
            'status': 'error',
            'error_description': 'This course cannot be found'
        }
        return None, False, error

def get_content(content_id):
    try:
        return Content.objects.get(id=content_id), True, None
    except Content.DoesNotExist:
        error = {
            'status': 'error',
            'error_description': 'This content cannot be found'
        }
        return None, False, error


def allowed_to_access_content(user, content):
    if content.can_access(user):
        return True
    return False

def allowed_to_access_course(user, course):
    if course.can_access(user):
        return True
    return False

def is_enrolled(user, course):
    return user.is_student and user.student_info.is_enrolled(course)

errors = {
    'content_not_found': {
            'status': 'error',
            'error_description': 'This content cannot be found'
        }
}
