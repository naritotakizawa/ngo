from ngo.urls import url
from tests.project1.app1 import views

app_name = 'app1'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^no/template/$', views.no_template, name='no_template'),
]
