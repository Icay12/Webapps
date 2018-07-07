from django.conf.urls import include, url
from bs_addrbook import views

urlpatterns = [
    url(r'^$', views.search),
    url(r'^bs_addrbook/', include('bs_addrbook.urls')),
]
