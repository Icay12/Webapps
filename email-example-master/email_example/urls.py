from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from email_example import views as my_views

urlpatterns = [
    url(r'^register$', my_views.register, name='register'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'email_example/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    # The following URL should match any username valid in Django and
    # any token produced by the default_token_generator
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9]+)/(?P<token>[a-z0-9\-]+)$',
        my_views.confirm_registration, name='confirm'),
]

