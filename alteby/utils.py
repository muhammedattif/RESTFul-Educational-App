
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

error_messages = {
    'content_not_found': 'This content cannot be found',
    'course_not_found': 'This course cannot be found',
    'access_denied': 'You don\'t have access to this resourse!, enroll this course to see its content.',
    'required_fields': 'Some fields are required.',
    'quiz_not_found': 'This content does not has any quizzes.',
    'question_not_found': 'One of the questions does not exists.',
    'choice_not_found': 'Selected answers must be one of the choices.',
    'page_access_denied': 'You don\'t have access to preview this page.',
    'empty_quiz_answers': "Quiz answers cannot be empty."
}

success_messages = {
    'quiz_answer_submitted': "Quiz answers has been recorded.",
    'enrolled': "Course Successfully Enrolled!"
}
