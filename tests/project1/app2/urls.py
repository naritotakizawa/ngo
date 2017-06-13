from ngo.urls import url
from tests.project1.app2 import views

app_name = 'app2'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^hello/(?P<name>\w+)/$', views.hello, name='hello'),
]
