"""テンプレートエンジンに関するモジュール."""
import os
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

        def render(self, request, context=None):
            """テンプレートの描画."""
            if context is None:
                context = {}
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

    class Template:
        """標準のTemplateクラス."""

        def __init__(self, template):
            """init."""
            self.template = template

        def render(self, request, context=None):
            """描画。.format_mapを行うだけ."""
            if context is None:
                context = {}
            context['request'] = request
            return self.template.format_map(context)

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
