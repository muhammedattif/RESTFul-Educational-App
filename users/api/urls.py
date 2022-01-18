from django.urls import path, include
from payment.api.views import CoursesEnrollments
from .views import SignIn, SignUp, ProfileDetail, EnrolledCourses
app_name = 'users'

urlpatterns = [
    # users APIs routes
    path('<int:user_id>/enrollments', CoursesEnrollments.as_view(), name="courses_enrollments"),
    path('profile/', ProfileDetail.as_view(), name="profile"),
    path('<int:user_id>/enrolled-courses/', EnrolledCourses.as_view(), name="enrolled-courses"),

    # Authentication Routes
    path('signin', SignIn.as_view(), name="signin"),
    path('signup', SignUp.as_view(), name="singup")
  ]
