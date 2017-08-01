from ngo.urls import url
from . import views

app_name = 'app'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]