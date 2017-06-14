"""URLに関するモジュール."""
from importlib import import_module
import re

from ngo.conf import settings
from ngo.exceptions import NoReverseMatch, Resolver404


def normalize(url_string):
    r"""URLの正規化を行う.

    >>> ^app2/^hello/user/(?P<name>\w+)/(?P<pk>\d+)/$
    /app2/hello/user/{name}/{pk}/

    >>> ^app2/^hello/(?P<name>\w+)/$
    /app2/hello/{name}/

    >>> ^^$
    /

    >>> ^^hello/$
    /hello/

    """
    url_string = url_string.replace('^', '')
    url_string = url_string.replace('$', '')
    if not url_string.startswith('/'):
        url_string = '/' + url_string

    # /app/(?P<name>\w+)/の、()部分
    base_regex = r'\(.*?{}.*?\)'

    # ()部分の、更に<name>部分。
    kwargs_regex = r'\<(?P<kwargs>.*?)\>'
    regex = base_regex.format(kwargs_regex)
    matches = re.finditer(regex, url_string)
    replaces = []

    # /app/(?P<name>\w+)/を、/app/{name}/のように変換していく
    for match in matches:
        result = (match.group(), match.group('kwargs'))
        replaces.append(result)

    for pat, kwarg in replaces:
        url_string = url_string.replace(pat, '{' + kwarg + '}')

    return url_string


def include(urlconf_module):
    """他のurls.pyの設定を読み込む."""
    # 'app.urls'のような文字列は、実際に読み込みmoduleオブジェクトにする
    if isinstance(urlconf_module, str):
        urlconf_module = import_module(urlconf_module)

    app_name = getattr(urlconf_module, 'app_name')
    return urlconf_module, app_name


def url(regex, view, name=None):
    """RegexURLPatternかRegexURLResolverを返す."""
    # include じゃない場合
    if callable(view):
        return RegexURLPattern(regex, view, url_name=name)

    # includeの場合。viewはurlconf_module, app_name のタプルとなっている
    else:
        urlconf_module, app_name = view
        return RegexURLResolver(regex, urlconf_module, app_name=app_name)


def get_resolver():
    """RegexURLResolverオブジェクトを返す."""
    # settings.pyの'project.urls'という文字列を、モジュールとしてimport
    urlconf_module = import_module(settings.ROOT_URLCONF)
    return RegexURLResolver(r'^/', urlconf_module)


def reverse(viewname, **kwargs):
    """appname:urlname をurlへ変換する."""
    app_name, url_name = viewname.split(':')
    resolver = get_resolver()

    for url_resolver_instance in resolver.url_patterns():
        # 各RegexURLResolverインスタンスの、app_nameが一致しているものを探す
        if app_name == url_resolver_instance.app_name:
            parent_pattern = url_resolver_instance.regex.pattern

            # RegexURLPatternインスタンスの、url_nameが一致しているものを探す
            for url_pattern_instanse in url_resolver_instance.url_patterns():
                if url_name == url_pattern_instanse.url_name:
                    pattern = url_pattern_instanse.regex.pattern

                    # それぞれのregex部分の文字列をnormalizeへ渡し、正規化する
                    url = normalize(parent_pattern + pattern)

                    # pk=1 などがあれば、あてはめる
                    if kwargs:
                        url = url.format(**kwargs)
                    return url

    else:
        raise NoReverseMatch('{}が見つかりません'.format(viewname))


class ResolverMatch:
    """resolveで返されるオブジェクト.

    URLの紐付けを行い、マッチした結果があればこのオブジェクトが返されます
    funcにはview関数、kwargsには(?P<pk>[0-9])等でマッチした{'pk': 1}の辞書
    url_name、app_nameはそれぞれ'app:home'のapp、home部分が入っています。

    """

    def __init__(self, func, kwargs, url_name, app_name):
        """init."""
        self.func = func
        self.kwargs = kwargs
        self.url_name = url_name
        self.app_name = app_name

    def __getitem__(self, index):
        """callback, callback_kwargs = ResolverMatch() ができるようになる."""
        return (self.func, self.kwargs)[index]

    def __repr__(self):
        """repr."""
        return '<ResolverMatch {}:{}>'.format(
            self.app_name, self.url_name
        )


class RegexURLPattern:
    """url(r'^$', views.home, name='home')を変換したオブジェクト."""

    def __init__(self, regex, callback, url_name):
        """init."""
        self.regex = re.compile(regex)
        self.callback = callback
        self.url_name = url_name

    def __repr__(self):
        """repr."""
        return '<RegexURLPattern {} {}>'.format(
            self.url_name, self.regex.pattern
        )

    def resolve(self, path, app_name):
        """URLの解決を行う."""
        match = self.regex.search(path)
        if match:
            kwargs = match.groupdict()
            return ResolverMatch(
                self.callback, kwargs,
                url_name=self.url_name, app_name=app_name
            )


class RegexURLResolver:
    """url(r'^', include('app.urls'))を変換したオブジェクト."""

    def __init__(self, regex, urlconf_name, app_name=None):
        """init."""
        self.regex = re.compile(regex)
        self.urlconf_name = urlconf_name
        self.app_name = app_name

    def __repr__(self):
        """repr."""
        return '<RegexURLResolver {} {}>'.format(
            self.app_name, self.regex.pattern
        )

    def resolve(self, path, app_name=None):
        """URLの解決を行う."""
        path = str(path)
        match = self.regex.search(path)
        if match:
            # 例として/app/path で/appがマッチし、/pathがnew_pathへ入る
            new_path = path[match.end():]

            # urlpatternsの中のRegexURLResolver、RegexURLPatternが渡され
            # 再帰的にresolveメソッドが呼び出される
            for pattern in self.url_patterns():
                resolver_match = pattern.resolve(new_path, self.app_name)
                if resolver_match:
                    return resolver_match
            # URL解決できなかった場合
            else:
                raise Resolver404('URL Not Found {}'.format(path))

    def url_patterns(self):
        """urls.pyの、urlspatternsリストを返す."""
        patterns = getattr(self.urlconf_name, 'urlpatterns')
        return patterns
