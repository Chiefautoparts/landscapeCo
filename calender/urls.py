from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^calendar/$', views.show, name='show')
]