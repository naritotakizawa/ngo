"""テンプレートエンジンに関するモジュール."""
import os
from ngo.exceptions import TemplateDoesNotExist


class BaseEngine:
    """テンプレートエンジンの抽象基底クラス
    
    独自のテンプレートエンジンを作成する場合は、このクラスを継承し、
    find_templateメソッドとTemplateクラスを上書きしてください。
    
    """
    
    class Template:
        """Template本体のラッパーとして機能します.
        
        サブクラスで上書きしてください。
        BaseEngineのget_templateメソッドでこのインスタンスを返し、renderメソッド
        を呼び出して使うことを想定しています。

        """
        pass

    def __init__(self, dirs):
        self.dirs = dirs

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def get_template_or_src(self, template_name):
        """テンプレートか、又はソース等を返す.
        
        サブクラスで上書きしてください。
        Templateクラスをインスタンス化する際の、引数になります。

        """
        pass

    def get_template(self, template_name):
        template_or_src = self.get_template_or_src(template_name)
        return self.Template(template_or_src)

class Jinja2(BaseEngine):
    """jinja2を使ったテンプレートエンジン."""

    class Template:
        def __init__(self, template):
            self.template = template

        def render(self, request, context=None):
            if context is None:
                context = {}
            context['request'] = request
            return self.template.render(context)

    def __init__(self, dirs):
        import jinja2
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(dirs),
            autoescape=True,
        )        

    def get_template_or_src(self, template_name):
        return self.env.get_template(template_name)


class NgoTemplates(BaseEngine):
    """Ngoフレームワークデフォルトのテンプレートエンジン.

    context = {'name': 'narito'}
    'name:{name}'.format_map(context)
    のようにしているだけです。

    """
    class Template:
        def __init__(self, template):
            self.template = template

        def render(self, request, context=None):
            if context is None:
                context = {}
            context['request'] = request
            return self.template.format_map(context)

    def get_template_or_src(self, template_name):
        for template_dir in self.dirs:
            template_path = os.path.join(template_dir, template_name)
            try:
                with open(template_path, 'r', encoding='utf-8') as fp:
                    return fp.read()
            except FileNotFoundError:
                pass
        else:
            raise TemplateDoesNotExist(f'{template_name} Not Found')