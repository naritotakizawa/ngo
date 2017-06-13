"""
from ngo.urls import url, include

urlpatterns = [
    url(r'^', include('app.urls')),
]
    
"""
from ngo.urls import url, include

urlpatterns = [
    url(r'^test_app2/', include('tests.test_app2.urls')),
    url(r'^', include('tests.test_app1.urls')),
]
    
