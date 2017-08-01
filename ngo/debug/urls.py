from ngo.conf import settings
from ngo.urls import url
from . import views

app_name = 'debug'

static_regx = r'^{0}/(?P<file_path>.*)/$'.format(settings.STATIC_URL)
media_regx = r'^{0}/(?P<file_path>.*)/$'.format(settings.MEDIA_URL)

urlpatterns = [
    url(static_regx, views.static, name=settings.STATIC_URL),
    url(media_regx, views.media, name=settings.MEDIA_URL),
]
