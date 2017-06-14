import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'app1',
    'app2',
]

ROOT_URLCONF = 'tests.project1.project.urls'

WSGI_APPLICATION = [
    'ngo.wsgi.RedirectApp',
    'ngo.wsgi.WSGIHandler',
]


TEMPLATES = ('ngo.backends.NgoTemplates', [])
# TEMPLATES = ('ngo.backends.Jinja2', [])