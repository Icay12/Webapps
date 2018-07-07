from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^add-item$', views.add_item),
    url(r'^delete-item$', views.delete_item),
]
