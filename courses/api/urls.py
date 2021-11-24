from django.urls import path, include
from .views import CourseList, CourseDetail, UpdateCourseProgress, ContentList, ContentDetail, CourseComments, CourseFeedbacks, ContentComments, QuizDetail, CourseAttachement, ContentAttachement

app_name = 'courses'

urlpatterns = [
  # courses APIs routes
  path('', CourseList.as_view(), name='courses'),

  # Courses API
  path('<int:course_id>/', CourseDetail.as_view(), name='course'),
  path('<int:course_id>/feedbacks/', CourseFeedbacks.as_view(), name='course_feedbacks'),
  path('<int:course_id>/comments', CourseComments.as_view(), name='course_comments'),
  path('<int:course_id>/quiz', QuizDetail.as_view(), name='course_quiz'),
  path('<int:course_id>/attachements', CourseAttachement.as_view(), name='course_attachment'),

  # Content API
  path('<int:course_id>/contents/', ContentList.as_view(), name='contents'),
  path('<int:course_id>/contents/<int:content_id>', ContentDetail.as_view(), name='content'),
  path('<int:course_id>/contents/<int:content_id>/mark_as_read', UpdateCourseProgress.as_view(), name='mark_as_read'),
  path('<int:course_id>/contents/<int:content_id>/comments', ContentComments.as_view(), name='content_comments'),
  path('<int:course_id>/contents/<int:content_id>/quiz', QuizDetail.as_view(), name='content_quiz'),
  path('<int:course_id>/contents/<int:content_id>/attachements', ContentAttachement.as_view(), name='content_attachment'),


]
