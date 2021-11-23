from django.urls import path, include
from payment.api.views import CoursesEnrollments
app_name = 'users'

urlpatterns = [
    # users APIs routes
    path('<int:user_id>/enrollments', CoursesEnrollments.as_view(), name="courses_enrollments")
  ]
