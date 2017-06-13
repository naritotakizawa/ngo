import os
import pytest

os.environ.setdefault('NGO_SETTINGS_MODULE', 'tests.test_project.settings')

from ngo.wsgi import get_wsgi_application, cast_finish_response
from ngo.urls import reverse


def test_access():
    """テストのサンプル。レスポンスヘッダー、本文を確認する"""
    wsgi_app = get_wsgi_application()
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': reverse('test_app1:home'),
        'QUERY_STRING': '',
    }
    start_response = lambda x, y: None
    response = wsgi_app(environ, start_response)
    response_headers = [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', '17'),
    ]
    assert response.headers == response_headers
    assert [b'Here is test_app1'] == list(response)
    