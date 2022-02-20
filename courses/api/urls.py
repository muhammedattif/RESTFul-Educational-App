from django.urls import path, include
from .views import (
CourseList, CourseUnitsList, UnitDetail, TopicList, TopicDetail,
FeaturedCoursesList, CourseDetail,
TrackCourseActivity, ContentList,
ContentDetail, CourseComments,
CourseFeedbacks, ContentComments,
QuizDetail, CourseQuizAnswer, ContentQuizAnswer,
CourseQuizResult, ContentQuizResult,
CourseAttachement, ContentAttachement
)

app_name = 'courses'

urlpatterns = [
  # courses APIs routes
  path('', CourseList.as_view(), name='courses'),

  # Courses API
  path('<int:course_id>/', CourseDetail.as_view(), name='course'),
  path('featured/', FeaturedCoursesList.as_view(), name='featured-course'),
  path('<int:course_id>/feedbacks/', CourseFeedbacks.as_view(), name='course_feedbacks'),
  path('<int:course_id>/comments', CourseComments.as_view(), name='course_comments'),
  path('<int:course_id>/quiz', QuizDetail.as_view(), name='course_quiz'),
  path('<int:course_id>/quiz/result', CourseQuizResult.as_view(), name='course_quiz_result'),
  path('<int:course_id>/quiz/answer', CourseQuizAnswer.as_view(), name='course_quiz_answer'),
  path('<int:course_id>/attachements', CourseAttachement.as_view(), name='course_attachment'),

  # Units API
  path('<int:course_id>/units/', CourseUnitsList.as_view(), name='units'),
  path('<int:course_id>/units/<int:unit_id>', UnitDetail.as_view(), name='unit'),
  # Topics API
  path('<int:course_id>/units/<int:unit_id>/topics', TopicList.as_view(), name='topics'),
  path('<int:course_id>/units/<int:unit_id>/topics/<int:topic_id>', TopicDetail.as_view(), name='topic-detail'),

  # Content API
  path('<int:course_id>/contents/', ContentList.as_view(), name='contents'),
  path('<int:course_id>/contents/<int:content_id>', ContentDetail.as_view(), name='content'),
  path('<int:course_id>/contents/<int:content_id>/mark_as_read', TrackCourseActivity.as_view(), name='mark_as_read'),
  path('<int:course_id>/contents/<int:content_id>/comments', ContentComments.as_view(), name='content_comments'),
  path('<int:course_id>/contents/<int:content_id>/quiz', QuizDetail.as_view(), name='content_quiz'),
  path('<int:course_id>/contents/<int:content_id>/quiz/result', ContentQuizResult.as_view(), name='content_quiz_result'),
  path('<int:course_id>/contents/<int:content_id>/quiz/answer', ContentQuizAnswer.as_view(), name='content_quiz_answer'),
  path('<int:course_id>/contents/<int:content_id>/attachements', ContentAttachement.as_view(), name='content_attachment'),


]
