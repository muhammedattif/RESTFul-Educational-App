from django.urls import path, include

app_name = 'users'

urlpatterns = [
    # Account APIs
    path('api', include('users.api.urls', 'users_api')),
  ]
