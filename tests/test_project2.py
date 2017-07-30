"""project1のテンプレートエンジンをjinja2にしたproject2の機能をテストする"""
import os
os.environ['NGO_SETTINGS_MODULE'] = 'tests.project2.project.settings'
import pytest
from ngo import conf, template, urls, wsgi
from ngo.exceptions import Resolver404, NoReverseMatch, TemplateDoesNotExist


def setup_module(module):
    import importlib
    os.environ['NGO_SETTINGS_MODULE'] = 'tests.project2.project.settings'
    importlib.reload(conf)
    importlib.reload(template)
    importlib.reload(urls)
    importlib.reload(wsgi)


def test_app1_home():
    """/ へアクセス"""
    url = urls.reverse('app1:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
    url = urls.reverse('app2:home')
    assert url == '/app2/'
    
    wsgi_app = wsgi.get_wsgi_application()
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
    url = urls.reverse('app2:hello', name='narito')
    assert url == '/app2/hello/narito/'

    wsgi_app = wsgi.get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '25'),
    ]
    assert response.headers == response_headers
    assert [b'<html>Hello narito</html>'] == list(response)


def test_app2_hello():
    """/app2/hello/ へアクセス (見つからない)"""
    url = urls.reverse('app2:hello')
    assert url == '/app2/hello/{name}/'

    wsgi_app = wsgi.get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/app2/hello/',
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    with pytest.raises(Resolver404) as excinfo:
        response = wsgi_app(environ, start_response)
    assert 'URL Not Found app2/hello/' == str(excinfo.value)


def test_app1_aiueo():
    """/aiueo/ へアクセス (見つからない)"""
    
    with pytest.raises(NoReverseMatch) as excinfo:
        url = urls.reverse('app1:aiueo')
    assert 'app1:aiueoが見つかりません' == str(excinfo.value)

    wsgi_app = wsgi.get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/aiueo/',
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    with pytest.raises(Resolver404) as excinfo:
        response = wsgi_app(environ, start_response)
    assert 'URL Not Found aiueo/' == str(excinfo.value)


def test_redirect():
    """/app2 へアクセス (リダイレクト)"""
    
    wsgi_app = wsgi.get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/app2',
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    assert [b''] == response
