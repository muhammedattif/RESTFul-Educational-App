from django.urls import path, include
from .views import get_courses, get_course

app_name = 'courses'

urlpatterns = [
  # courses APIs routes
  path('', get_courses, name='courses'),
  path('<int:course_id>/', get_course, name='course'),
]
