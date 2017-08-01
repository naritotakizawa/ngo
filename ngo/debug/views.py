import mimetypes
import os
from ngo.conf import settings
from ngo.exceptions import Resolver404
from ngo.response import HttpResponse


# settings.pyのSTATICFILES_DIRSと各アプリケーションのstaticディレクトリ
static_dirs = settings.STATICFILES_DIRS or []
for app in settings.INSTALLED_APPS:
    app_path = os.path.join(settings.BASE_DIR, app)
    static_dir = os.path.join(app_path, 'static')
    if os.path.isdir(static_dir):
        static_dirs.append(static_dir)


def static(request, file_path):
    """staticなファイルを配信するビュー関数."""
    for static_dir in static_dirs:
        path = os.path.join(static_dir, file_path)
        if os.path.isfile(path):
            with open(path, 'rb') as file:
                content = file.read()
            content_type = mimetypes.guess_type(file_path)[0]
            return HttpResponse(content, content_type, 200)
    raise Resolver404('URL Not Found {}'.format(request.path_info))


def media(request, file_path):
    """mediaファイルを配信するビュー関数."""
    path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.isfile(path):
        with open(path, 'rb') as file:
            content = file.read()
        content_type = mimetypes.guess_type(file_path)[0]
        return HttpResponse(content, content_type, 200)
    raise Resolver404('URL Not Found {}'.format(request.path_info))
