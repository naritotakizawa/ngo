"""
from ngo.urls import url, include

urlpatterns = [
    url(r'^', include('app.urls')),
]
    
"""
from ngo.urls import url, include

urlpatterns = [
    url(r'^app2/', include('tests.project2.app2.urls')),
    url(r'^', include('tests.project2.app1.urls')),
]
    
