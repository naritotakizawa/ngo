"""HTTPレスポンスに関するモジュール."""
from http.client import responses
from wsgiref.headers import Headers

from ngo.wsgi import cast_finish_response


class HttpResponse:
    """HTTPレスポンス情報を格納するクラス."""

    def __init__(self, content=b'',
                 content_type='text/html', status_code=200):
        """init."""
        if isinstance(content, bytes):
            self.content = content
        elif isinstance(content, str):
            self.content = content.encode('utf-8')

        self.content_type = '{}; charset=UTF-8'.format(
            content_type
        )

        self.status_code = status_code
        self.reason_phrase = responses.get(status_code, 'Unknown Status Code')
        self.headers = [
            ('Content-Type', self.content_type),
            ('Content-Length', str(len(self.content)))
        ]
        self.headers_dict = Headers(self.headers)

    def __repr__(self):
        """repr."""
        return '<HttpResponse {} {}>'.format(
            self.content_type, self.status_code
        )

    def __iter__(self):
        """iter."""
        return cast_finish_response(self.content)
