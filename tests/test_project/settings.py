import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'test_app1',
    'test_app2',
]

ROOT_URLCONF = 'tests.test_project.urls'

WSGI_APPLICATION = [
    'ngo.wsgi.RedirectApp',
    'ngo.wsgi.WSGIHandler',
]


TEMPLATES = ('ngo.backends.NgoTemplates', [])
# TEMPLATES = ('ngo.backends.Jinja2', [])
