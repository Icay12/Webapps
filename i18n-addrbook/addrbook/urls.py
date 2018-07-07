from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from addrbook import views as addrbook_views

urlpatterns = [
    url(r'^$', addrbook_views.search, name='home'),
    url(r'^search$', addrbook_views.search, name='search'),
    url(r'^create$', addrbook_views.create, name='create'),
    url(r'^delete/(\d+)$', addrbook_views.delete, name='delete'),
    url(r'^edit/(\d+)$', addrbook_views.edit, name='edit'),
    url(r'^register$', addrbook_views.register, name='register'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'addrbook/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]

