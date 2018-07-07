from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.search, name='home'),
    url(r'^search$', views.search, name='search'),
    url(r'^create$', views.create, name='create'),
    url(r'^delete/(\d+)$', views.delete, name='delete'),
    url(r'^edit/(\d+)$', views.edit, name='edit'),
    url(r'^register$', views.register, name='register'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'addrbook/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]

