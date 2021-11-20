from django.urls import path, include
from .views import CourseList, CourseDetail, QuizDetail

app_name = 'courses'

urlpatterns = [
  # courses APIs routes
  path('', CourseList.as_view(), name='courses'),
  path('<int:course_id>/', CourseDetail.as_view(), name='course'),
  path('<int:course_id>/quiz', QuizDetail.as_view(), name='course_quiz'),
  path('<int:course_id>/content/<int:content_id>/quiz', QuizDetail.as_view(), name='content_quiz'),


]
