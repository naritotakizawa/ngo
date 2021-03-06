"""ユーザー設定用モジュール."""
import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'app1',
    'app2',
]

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = [
    # 'wsgiref.validate.validator',
    'ngo.wsgi.RedirectApp',
    'ngo.wsgi.WSGIHandler',
]
"""
以下のように読み込まれていきます
app = None
app = WSGIHandler(None)
app = RedirectApp(app)
app = validator(app)
"""

TEMPLATES = ('ngo.backends.Ngo', [])
"""
TEMPLATES = (
    'ngo.backends.Ngo',
    [os.path.join(BASE_DIR, 'template'), os.path.join(BASE_DIR, 'template2')]
)

"""
# TEMPLATES = ('ngo.backends.Jinja2', [])


STATICFILES_DIRS = None
"""
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), os.path.join(BASE_DIR, 'static2')
]
"""
STATIC_URL = 'static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media'
