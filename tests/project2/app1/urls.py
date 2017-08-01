from ngo.urls import url
from . import views

app_name = 'app1'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^no/template/$', views.no_template, name='no_template'),
]
