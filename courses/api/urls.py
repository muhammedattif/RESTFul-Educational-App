from django.urls import path, include
from .views import CourseList, CourseDetail

app_name = 'courses'

urlpatterns = [
  # courses APIs routes
  path('', CourseList.as_view(), name='courses'),
  path('<int:course_id>/', CourseDetail.as_view(), name='course'),

]
