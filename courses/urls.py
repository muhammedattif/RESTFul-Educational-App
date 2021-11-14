from django.urls import path, include

app_name = 'courses'

urlpatterns = [
    # Account APIs
    path('api', include('courses.api.urls', 'courses_api')),
  ]
