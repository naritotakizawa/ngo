"""どこに入れるべきか悩んでいるテスト"""
import os
import io
import sys
import pytest


def setup_module(module):
    current = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current, 'project1')
    sys.path.insert(0, project_root)
    os.environ['NGO_SETTINGS_MODULE'] = 'project.settings'

    from ngo.conf import settings
    setattr(module, 'settings', settings)
    
    from ngo.template import HttpResponse
    setattr(module, 'HttpResponse', HttpResponse)
    
    from ngo.urls import reverse, ResolverMatch, RegexURLPattern, RegexURLResolver
    setattr(module, 'reverse', reverse)
    setattr(module, 'ResolverMatch', ResolverMatch)
    setattr(module, 'RegexURLPattern', RegexURLPattern)
    setattr(module, 'RegexURLResolver', RegexURLResolver)
    
    from ngo.wsgi import get_wsgi_application, WSGIRequest, cast_finish_response
    setattr(module, 'get_wsgi_application', get_wsgi_application)
    setattr(module, 'WSGIRequest', WSGIRequest)
    setattr(module, 'cast_finish_response', cast_finish_response)

    from ngo.exceptions import Resolver404, NoReverseMatch, TemplateDoesNotExist
    setattr(module, 'Resolver404', Resolver404)
    setattr(module, 'NoReverseMatch', NoReverseMatch)
    setattr(module, 'TemplateDoesNotExist', TemplateDoesNotExist)

    from ngo.utils import MultiValueDict, FileWrapper
    setattr(module, 'MultiValueDict', MultiValueDict)
    setattr(module, 'FileWrapper', FileWrapper)

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


def test_conf():
    assert repr(settings) == '<Settings project.settings>'


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
    file_wrapper.save()
    with pytest.raises(IOError) as excinfo:
        file_wrapper.save()
    assert 'File exists.' == str(excinfo.value)
    
    path = os.path.join(settings.MEDIA_ROOT, 'a.txt')
    os.remove(path)
    