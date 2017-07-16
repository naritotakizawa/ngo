"""設定例.
urlpatterns = [
    url(r'^', include('app.urls')),
]
    
"""
from ngo.urls import url, include

urlpatterns = [
    url(r'^', include('tests.project3.app.urls')),
]
