from ngo.urls import url
from tests.test_app1 import views

app_name = 'test_app1'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
