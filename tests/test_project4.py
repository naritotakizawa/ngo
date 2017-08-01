"""project4の機能をテストする(静的ファイルの配信)"""
import os
import sys
import pytest


def setup_module(module):
    current = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current, 'project4')
    sys.path.insert(0, project_root)
    os.environ['NGO_SETTINGS_MODULE'] = 'project.settings'

    from ngo.conf import settings
    setattr(module, 'settings', settings)
    
    from ngo.urls import reverse
    setattr(module, 'reverse', reverse)
    
    from ngo.wsgi import get_wsgi_application
    setattr(module, 'get_wsgi_application', get_wsgi_application)

    from ngo.exceptions import Resolver404, NoReverseMatch, TemplateDoesNotExist
    setattr(module, 'Resolver404', Resolver404)
    setattr(module, 'NoReverseMatch', NoReverseMatch)
    setattr(module, 'TemplateDoesNotExist', TemplateDoesNotExist)

    import importlib
    from project import settings, urls
    importlib.reload(settings)
    importlib.reload(urls)

    from app1 import urls
    importlib.reload(urls)

    from app2 import urls
    importlib.reload(urls)

    from ngo import template, conf
    importlib.reload(conf)
    importlib.reload(template)
    
    from ngo.debug import views
    importlib.reload(views)


def teardown_module(module):
    sys.path.pop(0)
    os.environ.pop('NGO_SETTINGS_MODULE')


def test_app_home():
    """/ へアクセス"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '383'),
    ]
    assert response.headers == response_headers


def test_static1():
    """/static/app/css/a.css/ の配信確認."""
    url = reverse('debug:static', file_path='app/css/a.css')
    assert url == '/static/app/css/a.css/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/css; charset=UTF-8'),
        ('Content-Length', '37'),
    ]
    assert response.headers == response_headers


def test_static2():
    """/static/app/b.css/ の配信確認."""
    url = reverse('debug:static', file_path='app/b.css')
    assert url == '/static/app/b.css/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/css; charset=UTF-8'),
        ('Content-Length', '37'),
    ]
    assert response.headers == response_headers


def test_static3():
    """/static/app/c.js/ の配信確認."""
    url = reverse('debug:static', file_path='app/c.js')
    assert url == '/static/app/c.js/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'application/javascript; charset=UTF-8'),
        ('Content-Length', '17'),
    ]
    assert response.headers == response_headers


def test_static4():
    """/static/app/js/d.js/ の配信確認."""
    url = reverse('debug:static', file_path='app/js/d.js')
    assert url == '/static/app/js/d.js/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'application/javascript; charset=UTF-8'),
        ('Content-Length', '17'),
    ]
    assert response.headers == response_headers


def test_static5():
    """/static/app/img/e.png/ の配信確認."""
    url = reverse('debug:static', file_path='app/img/e.png')
    assert url == '/static/app/img/e.png/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'image/png; charset=UTF-8'),
        ('Content-Length', '473831'),
    ]
    assert response.headers == response_headers

def test_static6():
    """/static/nofile/ の配信確認."""
    url = reverse('debug:static', file_path='nofile')
    assert url == '/static/nofile/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    with pytest.raises(Resolver404) as excinfo:
        response = wsgi_app(environ, start_response)
    assert 'URL Not Found /static/nofile/' == str(excinfo.value)


def test_media1():
    """/media/f.png の配信確認."""
    url = reverse('debug:media', file_path='f.png')
    assert url == '/media/f.png/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'image/png; charset=UTF-8'),
        ('Content-Length', '473831'),
    ]
    assert response.headers == response_headers


def test_media2():
    """/media/nofile の配信確認."""
    url = reverse('debug:media', file_path='nofile')
    assert url == '/media/nofile/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    with pytest.raises(Resolver404) as excinfo:
        response = wsgi_app(environ, start_response)
    assert 'URL Not Found /media/nofile/' == str(excinfo.value)
