from django.urls import path, include
from payment.api.views import CoursesEnrollments
from .views import SignIn, SignUp, ProfileDetail
app_name = 'users'

urlpatterns = [
    # users APIs routes
    path('<int:user_id>/enrollments', CoursesEnrollments.as_view(), name="courses_enrollments"),
    path('<str:username>/profile', ProfileDetail.as_view(), name="profile"),

    # Authentication Routes
    path('signin', SignIn.as_view(), name="signin"),
    path('signup', SignUp.as_view(), name="singup")
  ]
