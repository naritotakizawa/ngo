"""テンプレートエンジンに関するモジュール.

カスタムTemplateを作成する場合、renderメソッドを必ず実装するようにしてください

"""
from collections import ChainMap as _ChainMap
import os
import string
from ngo.exceptions import TemplateDoesNotExist


class Jinja2Template:
    """jinja2のTemplate."""

    def __init__(self, template_or_src):
        self.template_or_src = template_or_src

    def render(self, context):
        """テンプレートの描画."""
        return self.template.render(context)


class NgoTemplate(string.Template):
    """ngo標準のTemplateクラス."""

    # {{ }} で区切り、中身の空白は気にしない
    pattern = r'''
    \{\{[ ]*(?:
    (?P<escaped>\{\{[ ]*)|
    (?P<named>[_a-z][_a-z0-9]*)[ ]*\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)[ ]*\}\}|
    (?P<invalid>)
    )
    '''

    def __init__(self, template_or_src):
        self.template_or_src = template_or_src

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
        return self.pattern.sub(convert, self.template_or_src)

    def render(self, context):
        """描画。.safe_substituteを行うだけ."""
        return self.safe_substitute(context)


class Ngo:
    """Ngoデフォルトのテンプレートエンジン."""

    template = NgoTemplate

    def __init__(self, dirs):
        """初期化."""
        self.dirs = dirs

    def __repr__(self):
        """repr."""
        return '<{}>'.format(self.__class__.__name__)

    def get_template(self, template_name):
        # template_nameというファイルがあるか各ディレクトリを探す
        for template_dir in self.dirs:
            template_path = os.path.join(template_dir, template_name)
            try:
                # ファイルがあればソースを読み込み、Templateクラスを返す
                with open(template_path, 'r', encoding='utf-8') as fp:
                    src = fp.read()
                    return self.template(src)
            except FileNotFoundError:
                pass
        else:
            raise TemplateDoesNotExist('{} Not Found'.format(template_name))


class Jinja2(Ngo):
    """jinja2を使ったテンプレートエンジン."""

    template = Jinja2Template

    def __init__(self, dirs):
        """初期化."""
        import jinja2
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(dirs),
            autoescape=True,
        )

    def get_template(self, template_name):
        """Templateの引数、htmlソースや内部Templateを返す."""
        return self.env.get_template(template_name)
