"""どこに入れるべきか悩んでいるテスト"""
import os
os.environ['NGO_SETTINGS_MODULE'] = 'tests.project1.project.settings'
import io
import pytest
from ngo import conf, template
from ngo.conf import Settings
from ngo.urls import ResolverMatch, RegexURLPattern, RegexURLResolver
from ngo.utils import MultiValueDict, FileWrapper
from ngo.response import HttpResponse
from ngo.wsgi import WSGIRequest, cast_finish_response


def setup_module(module):
    import importlib
    os.environ['NGO_SETTINGS_MODULE'] = 'tests.project1.project.settings'
    importlib.reload(conf)
    importlib.reload(template)


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
    response = HttpResponse(b'', 'test/plain')
    assert repr(response) == '<HttpResponse test/plain; charset=UTF-8 200>'


def test_wsgi():
    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': '/hello/',
        'QUERY_STRING': '',
        'wsgi.input': io.BytesIO(),
    }
    start_response = lambda x, y: None
    request = WSGIRequest(environ)
    assert repr(request) == '<WSGIRequest POST /hello/>'
    assert request.GET == MultiValueDict()
    assert request.POST == MultiValueDict()
    assert request.FILES == MultiValueDict()
    
    data = list(cast_finish_response('Hello'))
    assert data == [b'Hello']
    
    data = list(cast_finish_response(['H', b'e', 'l', b'l', 'o']))
    assert data == [b'H', b'e', b'l', b'l', b'o']   

def test_utils():
    m_dict = MultiValueDict()
    assert repr(m_dict) == '<MultiValueDict: {}>'
    assert m_dict.get('no_key') == None
    assert m_dict.getlist('no-key', ['hello']) == ['hello']
    m_dict['list'] = []
    assert m_dict['list'] == []
    assert m_dict.get('list') == None
    assert m_dict.getlist('list') == []


    class Obj:
        pass

    file = io.StringIO()
    file.write('Hello utils')
    obj = Obj()
    obj.file = file
    obj.filename = 'a.txt'
    
    file_wrapper = FileWrapper(obj)
    file_wrapper.save('tests')
    with pytest.raises(IOError) as excinfo:
        file_wrapper.save('tests')
    assert 'File exists.' == str(excinfo.value)
    os.remove('tests/a.txt')
    