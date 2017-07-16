from ngo.urls import url
from tests.project3.app import views

app_name = 'app'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
