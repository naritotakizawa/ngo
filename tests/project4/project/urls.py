"""設定例.
urlpatterns = [
    url(r'^', include('app.urls')),
]
    
"""
from ngo.conf import settings
from ngo.urls import url, include

urlpatterns = [
    url(r'^', include('app.urls')),
]

if settings.DEBUG:
    debug_urls = url(r'^', include('ngo.debug.urls'))
    urlpatterns.insert(0, debug_urls)
