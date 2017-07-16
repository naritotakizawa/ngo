"""project3の機能をテストする(GET、POSTで贈られたデータの確認)"""
import os
import shutil
os.environ['NGO_SETTINGS_MODULE'] = 'tests.project3.project.settings'
import pytest
from ngo import conf, template, urls, wsgi, utils
from ngo.exceptions import Resolver404, NoReverseMatch, TemplateDoesNotExist
from ngo.utils import MultiValueDict, FileWrapper
from .tools import add_post_environ


def setup_module(module):
    import importlib
    os.environ['NGO_SETTINGS_MODULE'] = 'tests.project3.project.settings'
    importlib.reload(conf)
    importlib.reload(template)
    importlib.reload(urls)
    importlib.reload(wsgi)
    importlib.reload(utils)

def test_home_get1():
    """/ へアクセス"""
    url = urls.reverse('app:home')
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
    url = urls.reverse('app:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
    url = urls.reverse('app:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
    url = urls.reverse('app:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
    url = urls.reverse('app:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
    url = urls.reverse('app:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
        path = os.path.join(conf.settings.MEDIA_ROOT, filename)
        with open(path, 'r') as file:
            assert file.read() == content
    shutil.rmtree(conf.settings.MEDIA_ROOT)


def test_home_post5():
    """/へアクセス(ファイルを複数送信)"""
    url = urls.reverse('app:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
        path = os.path.join(conf.settings.MEDIA_ROOT, filename)
        with open(path, 'r') as file:
            assert file.read() == content
    shutil.rmtree(conf.settings.MEDIA_ROOT)


def test_home_post6():
    """/へアクセス(ファイルを複数送信とpostデータ)"""
    url = urls.reverse('app:home')
    assert url == '/'

    wsgi_app = wsgi.get_wsgi_application()
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
        path = os.path.join(conf.settings.MEDIA_ROOT, filename)
        with open(path, 'r') as file:
            assert file.read() == content
    shutil.rmtree(conf.settings.MEDIA_ROOT)