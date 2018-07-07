from django.conf.urls import include, url
from addrbook import views

urlpatterns = [
    url(r'^$', views.search),
    url(r'^addrbook/', include('addrbook.urls')),
]
