from .models import Lecture, Course, Unit, Topic
import alteby.utils as general_utils
from moviepy.editor import VideoFileClip, AudioFileClip

def get_course(course_id, prefetch_related=None, select_related=None):
    try:
        query = Course.objects
        if prefetch_related:
            query =  query.prefetch_related(*prefetch_related)
        if select_related:
            query =  query.select_related(*select_related)
        return query.get(id=course_id), True, None
    except Course.DoesNotExist:
        return None, False, general_utils.error('not_found')

def get_lecture(lecture_id, course_id=None, prefetch_related=None, select_related=None):
    try:
        query = Lecture.objects
        if prefetch_related:
            query = query.prefetch_related(*prefetch_related)
        if select_related:
            query = query.select_related(*select_related)
        if course_id:
            query = query.get(id=lecture_id, course_id=course_id)
        else:
            query = query.get(id=lecture_id)

        return query, True, None
    except Lecture.DoesNotExist:
        return None, False, general_utils.error('not_found')

def get_unit(filter_kwargs, prefetch_related=None, select_related=None):
    try:
        query = Unit.objects
        if prefetch_related:
            query = query.prefetch_related(*prefetch_related)
        if select_related:
            query = query.select_related(*select_related)
        return query.get(**filter_kwargs), True, None
    except Unit.DoesNotExist:
        return None, False, general_utils.error('not_found')


def get_object(model, filter_kwargs, prefetch_related=None, select_related=None):
    try:
        query = model.objects
        if prefetch_related:
            query = query.prefetch_related(*prefetch_related)
        if select_related:
            query = query.select_related(*select_related)
        return query.get(**filter_kwargs), True, None
    except model.DoesNotExist:
        return None, False, general_utils.error('not_found')

def allowed_to_access_lecture(user, lecture):
    if lecture.can_access(user) or is_enrolled(user, lecture.topic.unit.course):
        return True
    return False

def allowed_to_access_course(user, course):
    if course.can_access(user) or is_enrolled(user, course):
        return True
    return False

def is_enrolled(user, course):
    return user.is_student and user.student_info.is_enrolled(course)

def detect_video_duration(video_path):
    return VideoFileClip(video_path).duration
