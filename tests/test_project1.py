"""project1の機能をテストする"""
import os
import sys
import pytest


def setup_module(module):
    current = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current, 'project1')
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


def teardown_module(module):
    sys.path.pop(0)
    os.environ.pop('NGO_SETTINGS_MODULE')


def test_app1_home():
    """/ へアクセス"""
    url = reverse('app1:home')
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
        ('Content-Length', '12'),
    ]
    assert response.headers == response_headers
    assert [b'Here is app1'] == list(response)


def test_app2_home():
    """/app2/ へアクセス"""
    url = reverse('app2:home')
    assert url == '/app2/'
    
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
        ('Content-Length', '12'),
    ]
    assert response.headers == response_headers
    assert [b'Here is app2'] == list(response)


def test_app2_hello_narito():
    """/app2/hello/narito/ へアクセス"""
    url = reverse('app2:hello', name='narito')
    assert url == '/app2/hello/narito/'

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
        ('Content-Length', '12'),
    ]
    assert response.headers == response_headers
    assert [b'Hello narito'] == list(response)


def test_app2_hello():
    """/app2/hello/ へアクセス (見つからない)"""
    url = reverse('app2:hello')
    assert url == '/app2/hello/{name}/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/app2/hello/',
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    with pytest.raises(Resolver404) as excinfo:
        response = wsgi_app(environ, start_response)
    assert 'URL Not Found /app2/hello/' == str(excinfo.value)


def test_app1_aiueo():
    """/aiueo/ へアクセス (見つからない)"""
    
    with pytest.raises(NoReverseMatch) as excinfo:
        url = reverse('app1:aiueo')
    assert 'app1:aiueoが見つかりません' == str(excinfo.value)

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/aiueo/',
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    with pytest.raises(Resolver404) as excinfo:
        response = wsgi_app(environ, start_response)
    assert 'URL Not Found /aiueo/' == str(excinfo.value)


def test_redirect():
    """/app2 へアクセス (リダイレクト)"""
    
    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/app2',
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    assert [b''] == response
        

def test_app1_no_template():
    """/no/template へアクセス (テンプレートが見つからない)"""
    url = reverse('app1:no_template')
    assert url == '/no/template/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    with pytest.raises(TemplateDoesNotExist) as excinfo:
        response = wsgi_app(environ, start_response)
    assert 'app1/aaaaa.html Not Found' == str(excinfo.value)