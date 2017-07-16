"""WSGIに関するモジュール."""
import cgi
import importlib
from urllib import parse
from ngo.conf import settings
from ngo.urls import get_resolver
from ngo.utils import MultiValueDict, FileWrapper


def get_wsgi_application():
    """WSGIアプリケーションを返す.

    settings.pyの、WSGI_APPLICATIONリスト内にあるWSGIアプリケーションを
    次々に読み込んでいきます。

    読み込むWSGIアプリケーションは、クラスとして定義し、そのimportパスを
    'ngo.wsgi.RedirectApp'のように記載してください。

    """
    wsgi_app = None
    for wsgi_class_path in settings.WSGI_APPLICATION[::-1]:
        module_name, class_name = wsgi_class_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        wsgi_app = cls(wsgi_app)
    return wsgi_app


class WSGIRequest:
    """requestオブジェクトを作成するクラス."""

    def __init__(self, environ):
        """init."""
        self.environ = environ
        self.method = environ['REQUEST_METHOD'].upper()
        self.path_info = environ['PATH_INFO']

    @property
    def FILES(self):
        """request.FILESでアクセスされる."""
        if not hasattr(self, '_files'):
            self._load_post_and_files()
        return self._files

    @property
    def POST(self):
        """request.POSTでアクセスされる."""
        if not hasattr(self, '_post'):
            self._load_post_and_files()
        return self._post

    @property
    def GET(self):
        """request.GETでアクセスされる."""
        if not hasattr(self, '_get'):
            self._get = MultiValueDict()
            query = parse.parse_qs(self.environ['QUERY_STRING'])
            for key, value in query.items():
                # valueが空文字の場合があるので、その場合は空リストを入れる
                self._get[key] = value or []
        return self._get

    def _load_post_and_files(self):
        """postデータとアップロードファイルを取得する."""
        self._post = MultiValueDict()
        self._files = MultiValueDict()

        # GETパラメータを除外したenvironを作成し、cgi.FieldStorageに渡す
        post_environ = self.environ.copy()
        post_environ['QUERY_STRING'] = ''
        if self.method == 'POST':
            form = cgi.FieldStorage(
                fp=self.environ['wsgi.input'],
                environ=post_environ,
                keep_blank_values=True
            )
            for item in form.list:
                # ファイルの場合は_files(FILES)へ格納
                if item.filename:
                    self._files.appendlist(item.name, FileWrapper(item))

                # ファイルじゃなく、値が空文字じゃなければ_post(POST)へ
                elif item.value:
                    self._post.appendlist(item.name, item.value)

    def __repr__(self):
        """repr."""
        return '<WSGIRequest {} {}>'.format(
            self.method, self.path_info
        )


class WSGIHandler:
    """WSGIアプリケーションとなるクラス."""

    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        """ロジック上、引数としてNoneを受け取ることがあり、そのため上書き."""
        pass

    def __call__(self, environ, start_response):
        """WSGI-interface."""
        request = self.request_class(environ)
        response = self.get_response(request)
        status = '{} {}'.format(
            response.status_code, response.reason_phrase
        )
        start_response(status, response.headers)
        return response

    def get_response(self, request):
        """対応するviewを呼び出し、HttpResponseオブジェクトを返す."""
        resolver = get_resolver()
        resolver_match = resolver.resolve(request.path_info)
        callback, callback_kwargs = resolver_match
        # home_view(request, pk=1) のような呼び出しになる
        return callback(request, **callback_kwargs)


class RedirectApp:
    """条件によってリダイレクトを行うWSGIミドルウェア."""

    def __init__(self, application):
        """init."""
        self.application = application

    def __call__(self, environ, start_response):
        """パスの最後に「/」がなければ、/をつけてリダイレクトさせる."""
        path_info = environ['PATH_INFO']
        if path_info.endswith('/'):
            return self.application(environ, start_response)
        else:
            path_info += '/'
            start_response(
                '301 Moved Permanently',
                ('Location', path_info),
            )
            return [b'']


def cast_finish_response(content):
    """WSGIアプリケーションがreturnする値として正しい形に変換する.

    引数として、以下のようなデータを受け取ることができます。
    >>> case1 = 'Hello'
    >>> case2 = ['Hello']
    >>> case3 = ['H', 'e', 'l', 'l', 'o']
    >>> case4 = b'Hello'
    >>> case5 = [b'Hello']
    >>> case6 = [b'H', b'e', b'l', b'l', b'o']
    >>> case7 = ''
    >>> case8 = b''

    >>> list(cast_finish_response(case1))
    [b'Hello']

    >>> list(cast_finish_response(case2))
    [b'Hello']

    >>> list(cast_finish_response(case3))
    [b'H', b'e', b'l', b'l', b'o']

    >>> list(cast_finish_response(case4))
    [b'Hello']

    >>> list(cast_finish_response(case5))
    [b'Hello']

    >>> list(cast_finish_response(case6))
    [b'H', b'e', b'l', b'l', b'o']

    >>> list(cast_finish_response(case7))
    [b'']

    >>> list(cast_finish_response(case8))
    [b'']

    """
    if isinstance(content, bytes):
        yield content
    elif isinstance(content, str):
        yield content.encode('utf-8')
    else:
        for char in content:
            if isinstance(char, bytes):
                yield char
            else:
                yield char.encode('utf-8')
