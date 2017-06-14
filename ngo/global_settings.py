"""ベースとなる設定."""
BASE_DIR = None

INSTALLED_APPS = None

ROOT_URLCONF = None

WSGI_APPLICATION = [
    'ngo.wsgi.RedirectApp',
    'ngo.wsgi.WSGIHandler',
]

DEFAULT_CONTENT_TYPE = 'text/html'

TEMPLATES = ('ngo.backends.NgoTemplates', [])
