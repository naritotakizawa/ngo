from ngo.urls import url
from . import views

app_name = 'app2'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^hello/(?P<name>\w+)/$', views.hello, name='hello'),
]
