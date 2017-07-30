import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INSTALLED_APPS = [
    'app1',
    'app2',
]

ROOT_URLCONF = 'tests.project1.project.urls'

WSGI_APPLICATION = [
    #'wsgiref.validate.validator',
    'ngo.wsgi.RedirectApp',
    'ngo.wsgi.WSGIHandler',
]


TEMPLATES = ('ngo.backends.Ngo', [])

