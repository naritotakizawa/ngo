from ngo.urls import url
from tests.project2.app1 import views

app_name = 'app1'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]