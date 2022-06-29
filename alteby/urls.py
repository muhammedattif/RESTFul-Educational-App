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
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from alteby.error_views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main
    path('main', include('main.urls', 'main')),
    # Main
    path('api/main/', include('main.api.urls', 'main_apis')),

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

    # Playlists
    path('categories/', include('categories.urls', 'categories')),
    # Playlists APIs
    path('api/categories/', include('categories.api.urls', 'categories_api')),

    # Payment
    path('payment/', include('payment.urls', 'payment')),
    # Payment APIs
    path('api/payment/', include('payment.api.urls', 'payment_api')),
]

if not settings.DEBUG:
    urlpatterns += [
    # Debug tool Bar
    path('__debug__/', include(debug_toolbar.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Swagger
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]


admin.site.index_title = settings.SITE_INDEX_TITLE
admin.site.site_title = settings.SITE_TITLE
admin.site.site_header = settings.SITE_HEADER


# Errors Handlers
handler404 = custom_error_404
handler500 = custom_error_500
