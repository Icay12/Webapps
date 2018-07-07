from django.conf.urls import include, url
from picture_list import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^email-example/', include('email_example.urls')),
    url(r'^picture-list/', include('picture_list.urls')),
]
