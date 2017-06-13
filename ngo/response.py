"""HTTPレスポンスに関するモジュール."""
from http.client import responses
from wsgiref.headers import Headers

from ngo.wsgi import cast_finish_response
from ngo.conf import settings


class HttpResponse:
    """HTTPレスポンス情報を格納するクラス."""

    def __init__(self, content=b'',
                 content_type=None, status_code=200):
        if isinstance(content, bytes):
            self.content = content
        elif isinstance(content, str):
            self.content = content.encode('utf-8')

        if content_type is None:
            self.content_type = f'{settings.DEFAULT_CONTENT_TYPE}; charset=UTF-8'
        else:
            self.content_type = content_type
        self.status_code = status_code
        self.reason_phrase = responses.get(status_code, 'Unknown Status Code')
        self.headers = [
            ('Content-Type', self.content_type),
            ('Content-Length', str(len(self.content)))
        ]
        self.headers_dict = Headers(self.headers)

    def __repr__(self):
        return f'<HttpResponse {self.content_type} {self.status_code}>'

    def __iter__(self):
        return cast_finish_response(self.content)
