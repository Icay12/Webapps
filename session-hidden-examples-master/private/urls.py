from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^add-item$', views.add_item),
    url(r'^delete-all$', views.delete_all),
    url(r'^delete-item$', views.delete_item),
    url(r'^provide-name$', views.provide_name),
]
