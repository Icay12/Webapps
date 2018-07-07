from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from todolist2 import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^add-item$', views.add_item, name='add-item'),
    url(r'^delete-item/(?P<item_id>\d+)$', views.delete_item, name='delete-item'),
]
