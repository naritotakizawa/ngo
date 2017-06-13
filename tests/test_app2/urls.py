from ngo.urls import url
from tests.test_app2 import views

app_name = 'test_app2'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
