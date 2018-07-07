"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from hidden  import views as hidden_views
from welcome import views as welcome_views
from shared  import urls  as shared_urls
from private import urls  as private_urls

urlpatterns = [
    url(r'^$',        welcome_views.home),
    url(r'^hidden/',  hidden_views.hidden_demo),
    url(r'^shared/',  include(shared_urls)),
    url(r'^private/', include(private_urls)),
]
