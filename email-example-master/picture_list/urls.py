from django.conf.urls import include, url
from picture_list import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add-item$', views.add_item, name='add'),
    url(r'^delete-item/(?P<id>\d+)$', views.delete_item, name='delete'),
    url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'),
]
