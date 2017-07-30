"""テンプレートに関するモジュール."""
import importlib
import os
from ngo.conf import settings
from ngo.response import HttpResponse

# テンプレートエンジンをsettings.pyから取得する
module_name, class_name = settings.TEMPLATES[0].rsplit('.', 1)
module = importlib.import_module(module_name)
engine_class = getattr(module, class_name)


# settings.pyのDIRSに加え、各アプリケーションのtemplatesディレクトリをパスに
template_dirs = settings.TEMPLATES[1]
for app in settings.INSTALLED_APPS:
    app_path = os.path.join(settings.BASE_DIR, app)
    template_dir = os.path.join(app_path, 'templates')
    if os.path.isdir(template_dir):
        template_dirs.append(template_dir)


def add_default_context(request, context):
    """デフォルトコンテキストの作成."""
    context['request'] = request
    return context


def render(request, template_name, context=None,
           content_type='text/html', status=200):
    """HttpResponseを作成する."""
    # コンテキストの調整・デフォルトコンテキストの追加
    if context is None:
        context = {}
    context = add_default_context(request, context)

    # テンプレートの取得・描画
    engine = engine_class(template_dirs)
    template = engine.get_template(template_name)
    content = template.render(context)
    return HttpResponse(content, content_type, status)
