"""project3の機能をテストする(GET、POSTで贈られたデータやファイルの確認)"""
import os
import sys
import shutil
import pytest
from .tools import add_post_environ


CURRENT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(CURRENT, 'project3')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')


def setup_module(module):
    sys.path.insert(0, PROJECT_ROOT)
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

    from app import urls
    importlib.reload(urls)

    from ngo import template, conf, utils
    importlib.reload(conf)
    importlib.reload(template)
    importlib.reload(utils)
    

def teardown_module(module):
    sys.path.pop(0)
    os.environ.pop('NGO_SETTINGS_MODULE')


def test_home_get1():
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
        ('Content-Length', '905'),
    ]
    assert response.headers == response_headers
    assert '<p>text: None</p>'.encode('utf-8') in response.content
    assert '<p>text2: None</p>'.encode('utf-8') in response.content
    assert "<p>select: []</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: </p>'.encode('utf-8') in response.content
    assert '<p>ファイル名2: </p>'.encode('utf-8') in response.content


def test_home_get2():
    """/?text=1&text2=2&select=3&select=4 へアクセス"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': url,
        'QUERY_STRING': 'text=hello&text2=world&select=3&select=4',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '915'),
    ]
    assert response.headers == response_headers
    assert '<p>text: hello</p>'.encode('utf-8') in response.content
    assert '<p>text2: world</p>'.encode('utf-8') in response.content
    assert "<p>select: ['3', '4']</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: </p>'.encode('utf-8') in response.content
    assert '<p>ファイル名2: </p>'.encode('utf-8') in response.content


def test_home_post1():
    """/へアクセス(postデータなし)"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': url,
    }
    environ = add_post_environ(environ)
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '905'),
    ]
    assert response.headers == response_headers
    assert '<p>text: None</p>'.encode('utf-8') in response.content
    assert '<p>text2: None</p>'.encode('utf-8') in response.content
    assert "<p>select: []</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: </p>'.encode('utf-8') in response.content
    assert '<p>ファイル名2: </p>'.encode('utf-8') in response.content


def test_home_post2():
    """/へアクセス(postデータあり)"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': url,
    }

    data = [
        ('text', 'hello'), ('text2', 'world'), ('select', '3'), ('select', '4')
    ]
    environ = add_post_environ(environ, data=data)

    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '915'),
    ]
    assert response.headers == response_headers
    assert '<p>text: hello</p>'.encode('utf-8') in response.content
    assert '<p>text2: world</p>'.encode('utf-8') in response.content
    assert "<p>select: ['3', '4']</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: </p>'.encode('utf-8') in response.content
    assert '<p>ファイル名2: </p>'.encode('utf-8') in response.content


def test_home_post3():
    """/へアクセス(postとgetパラメータ、views.pyのロジックでpostデータ反映)"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': url,
        'QUERY_STRING': 'text=auaua&text2=oooo&select=1000&select=42',
    }

    data = [
        ('text', 'hello'), ('text2', 'world'), ('select', '3'), ('select', '4')
    ]
    environ = add_post_environ(environ, data=data)

    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '915'),
    ]
    assert response.headers == response_headers
    assert '<p>text: hello</p>'.encode('utf-8') in response.content
    assert '<p>text2: world</p>'.encode('utf-8') in response.content
    assert "<p>select: ['3', '4']</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: </p>'.encode('utf-8') in response.content
    assert '<p>ファイル名2: </p>'.encode('utf-8') in response.content


def test_home_post4():
    """/へアクセス(ファイルを一つ送信)"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': url,
    }
    files = [
        ('files', 'test1.txt', 'Hello Test'),
    ]
    environ = add_post_environ(environ, files=files)

    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '914'),
    ]
    assert response.headers == response_headers
    assert '<p>text: None</p>'.encode('utf-8') in response.content
    assert '<p>text2: None</p>'.encode('utf-8') in response.content
    assert "<p>select: []</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: test1.txt</p>'.encode('utf-8') in response.content
    assert '<p>ファイル名2: </p>'.encode('utf-8') in response.content
    for _, filename, content in files:
        path = os.path.join(MEDIA_ROOT, filename)
        with open(path, 'r') as file:
            assert file.read() == content
    shutil.rmtree(MEDIA_ROOT)


def test_home_post5():
    """/へアクセス(ファイルを複数送信)"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': url,
    }
    files = [
        ('files', 'test1.txt', 'Hello Test'),
        ('files2', 'test2.txt', 'Hello a'),
        ('files2', 'test3.txt', 'Hello i'),
        ('files2', 'test4.txt', 'Hello u'),
    ]
    environ = add_post_environ(environ, files=files)

    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '953'),
    ]
    assert response.headers == response_headers
    assert '<p>text: None</p>'.encode('utf-8') in response.content
    assert '<p>text2: None</p>'.encode('utf-8') in response.content
    assert "<p>select: []</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: test1.txt</p>'.encode('utf-8') in response.content
    assert "<p>ファイル名2: ['test2.txt', 'test3.txt', 'test4.txt']</p>".encode('utf-8') in response.content
    for _, filename, content in files:
        path = os.path.join(MEDIA_ROOT, filename)
        with open(path, 'r') as file:
            assert file.read() == content
    shutil.rmtree(MEDIA_ROOT)


def test_home_post6():
    """/へアクセス(ファイルを複数送信とpostデータ)"""
    url = reverse('app:home')
    assert url == '/'

    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': url,
    }
    data = [
        ('text', 'hello'), ('text2', 'world'), ('select', '3'), ('select', '4')
    ]
    files = [
        ('files', 'test1.txt', 'Hello Test'),
        ('files2', 'test2.txt', 'Hello a'),
        ('files2', 'test3.txt', 'Hello i'),
        ('files2', 'test4.txt', 'Hello u'),
    ]
    environ = add_post_environ(environ, files=files, data=data)

    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '963'),
    ]
    assert response.headers == response_headers
    assert '<p>text: hello</p>'.encode('utf-8') in response.content
    assert '<p>text2: world</p>'.encode('utf-8') in response.content
    assert "<p>select: ['3', '4']</p>".encode('utf-8') in response.content
    assert '<p>ファイル名: test1.txt</p>'.encode('utf-8') in response.content
    assert "<p>ファイル名2: ['test2.txt', 'test3.txt', 'test4.txt']</p>".encode('utf-8') in response.content
    for _, filename, content in files:
        path = os.path.join(MEDIA_ROOT, filename)
        with open(path, 'r') as file:
            assert file.read() == content
    shutil.rmtree(MEDIA_ROOT)
