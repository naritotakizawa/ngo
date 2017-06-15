"""どこに入れるべきか悩んでいるテスト"""
import importlib
import os
os.environ['NGO_SETTINGS_MODULE'] = 'tests.project1.project.settings'
from ngo.backends import BaseEngine
from ngo.conf import Settings
from ngo.urls import ResolverMatch, RegexURLPattern, RegexURLResolver
from ngo.response import HttpResponse
from ngo.wsgi import WSGIRequest, cast_finish_response

import importlib
from ngo import conf, template


def setup_module(module):
    os.environ['NGO_SETTINGS_MODULE'] = 'tests.project1.project.settings'
    importlib.reload(conf)
    importlib.reload(template)


def test_backends():
    base_engine = BaseEngine('.')
    template = base_engine.get_template('spam')
    assert repr(base_engine) == '<BaseEngine>'


def test_conf():
    settings = Settings()
    assert repr(settings) == '<Settings tests.project1.project.settings>'


def test_urls():
    resolver_match = ResolverMatch(lambda:None, {}, 'url', 'app')
    assert repr(resolver_match) == '<ResolverMatch app:url>'
    
    regex_url_pattern = RegexURLPattern(r'^', lambda:None, 'url')
    assert repr(regex_url_pattern) == '<RegexURLPattern url ^>'
    
    regex_url_resolver = RegexURLResolver(r'^', 'urls.py', 'app')
    assert repr(regex_url_resolver) == '<RegexURLResolver app ^>'


def test_response():
    response = HttpResponse(b'', 'test/plain; charset=UTF-8')
    assert repr(response) == '<HttpResponse test/plain; charset=UTF-8 200>'


def test_wsgi():
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': '/hello/',
        'wsgi.input': open('README.rst'),
    }
    start_response = lambda x, y: None
    request = WSGIRequest(environ)
    assert repr(request) == '<WSGIRequest POST /hello/>'
    
    data = list(cast_finish_response('Hello'))
    assert data == [b'Hello']
    
    data = list(cast_finish_response(['H', b'e', 'l', b'l', 'o']))
    assert data == [b'H', b'e', b'l', b'l', b'o']   
    