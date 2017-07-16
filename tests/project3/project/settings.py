"""ユーザー設定用モジュール."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INSTALLED_APPS = [
    'app',
]

ROOT_URLCONF = 'tests.project3.project.urls'

WSGI_APPLICATION = [
    'ngo.wsgi.RedirectApp',
    'ngo.wsgi.WSGIHandler',
]


TEMPLATES = ('ngo.backends.NgoTemplates', [])
# TEMPLATES = ('ngo.backends.Jinja2', [])