from django.conf.urls import include, url
from addrbook2 import views

urlpatterns = [
    url(r'^$', views.search, name='home'),
    url(r'^search$', views.search, name='search'),
    url(r'^create$', views.create, name='create'),
    url(r'^delete/(\d+)$', views.delete, name='delete'),
    url(r'^edit/(\d+)$', views.edit, name='edit'),
]

