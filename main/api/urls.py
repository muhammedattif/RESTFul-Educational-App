from django.urls import path
from .views import ContactUsView

app_name = 'main'

urlpatterns = [
    path('contactus', ContactUsView.as_view(), name='contactus'),
  ]
