from .models import Content


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


errors = {
    'content_not_found': {
            'status': 'error',
            'error_description': 'This content cannot be found'
        }
}