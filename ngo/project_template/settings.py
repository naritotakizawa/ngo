"""ユーザー設定用モジュール."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [

]

ROOT_URLCONF = '{project_name}.urls'

WSGI_APPLICATION = [
    'ngo.wsgi.RedirectApp',
    'ngo.wsgi.WSGIHandler',
]


TEMPLATES = ('ngo.backends.NgoTemplates', [])
# TEMPLATES = ('ngo.backends.Jinja2', [])
