"""alteby URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import debug_toolbar
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    # Users
    path('users', include('users.urls', 'users')),
    # Users APIs
    path('api/users/', include('users.api.urls', 'users_api')),

    # Courses
    path('courses/', include('courses.urls', 'courses')),
    # Courses APIs
    path('api/courses/', include('courses.api.urls', 'courses_api')),

    # Playlists
    path('playlists/', include('playlists.urls', 'playlists')),
    # Playlists APIs
    path('api/playlists/', include('playlists.api.urls', 'playlists_api')),
]
