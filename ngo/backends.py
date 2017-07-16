"""テンプレートエンジンに関するモジュール."""
from collections import ChainMap as _ChainMap
import os
import string
from ngo.exceptions import TemplateDoesNotExist


class BaseEngine:
    """テンプレートエンジンの抽象基底クラス.

    独自のテンプレートエンジンを作成する場合は、このクラスを継承し、
    find_templateメソッドとTemplateクラスを上書きしてください。

    """

    class Template:
        """Template本体のラッパーとして機能します.

        サブクラスで上書きしてください。
        BaseEngineのget_templateメソッドでこのインスタンスを返し、renderメソッド
        を呼び出して使うことを想定しています。

        """

        def __init__(self, template):
            """init."""
            self.template = template

    def __init__(self, dirs):
        """init."""
        self.dirs = dirs

    def __repr__(self):
        """repr."""
        return '<{}>'.format(self.__class__.__name__)

    def get_template_or_src(self, template_name):
        """Templateの引数、htmlソースや内部Templateを返す.

        サブクラスで上書きしてください。

        """
        pass

    def get_template(self, template_name):
        """renderを持つTemplateクラスを返す."""
        template_or_src = self.get_template_or_src(template_name)
        return self.Template(template_or_src)


class Jinja2(BaseEngine):
    """jinja2を使ったテンプレートエンジン."""

    class Template:
        """jinja2のTemplateクラス."""

        def __init__(self, template):
            """init."""
            self.template = template

        def render(self, request, context):
            """テンプレートの描画."""
            context['request'] = request
            return self.template.render(context)

    def __init__(self, dirs):
        """init."""
        import jinja2
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(dirs),
            autoescape=True,
        )

    def get_template_or_src(self, template_name):
        """Templateの引数、htmlソースや内部Templateを返す."""
        return self.env.get_template(template_name)


class NgoTemplates(BaseEngine):
    """Ngoフレームワークデフォルトのテンプレートエンジン.

    context = {'name': 'narito'}
    'name:{name}'.format_map(context)
    のようにしているだけです。

    """

    class Template(string.Template):
        """標準のTemplateクラス."""

        delimiter = '{{'
        pattern = r'''
        \{\{(?:
        (?P<escaped>\{\{)|
        (?P<named>[_a-z][_a-z0-9]*)\}\}|
        (?P<braced>[_a-z][_a-z0-9]*)\}\}|
        (?P<invalid>)
        )
        '''

        def safe_substitute(*args, **kws):
            if not args:
                raise TypeError(
                    "descriptor 'safe_substitute' of 'Template' object "
                    "needs an argument"
                )
            self, *args = args  # allow the "self" keyword be passed
            if len(args) > 1:
                raise TypeError('Too many positional arguments')
            if not args:
                mapping = kws
            elif kws:
                mapping = _ChainMap(kws, args[0])
            else:
                mapping = args[0]

            # Helper function for .sub()
            def convert(mo):
                named = mo.group('named') or mo.group('braced')
                if named is not None:
                    try:
                        return str(mapping[named])
                    except KeyError:
                        return ''
                if mo.group('escaped') is not None:
                    return self.delimiter
                if mo.group('invalid') is not None:
                    return mo.group()
                raise ValueError('Unrecognized named group in pattern',
                                 self.pattern)
            return self.pattern.sub(convert, self.template)

        def render(self, request, context):
            """描画。.safe_substituteを行うだけ."""
            return self.safe_substitute(context)

    def get_template_or_src(self, template_name):
        """htmlソースを返す."""
        for template_dir in self.dirs:
            template_path = os.path.join(template_dir, template_name)
            try:
                with open(template_path, 'r', encoding='utf-8') as fp:
                    return fp.read()
            except FileNotFoundError:
                pass
        else:
            raise TemplateDoesNotExist('{} Not Found'.format(template_name))
