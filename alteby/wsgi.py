"""
WSGI config for alteby project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
import environ
import os
from django.core.wsgi import get_wsgi_application

env = environ.Env()
# reading .env file
environ.Env.read_env()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alteby.settings.' + env('ENVIRONMENT'))

application = get_wsgi_application()
