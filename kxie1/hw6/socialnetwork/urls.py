from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.global_stream, name='home'),
    url(r'^globalstream$', views.global_stream, name='global'),
    url(r'^followerstream/(\w+)$', views.follower_stream, name='follower'),
    # url(r'^profile$', views.profile, name='profile'),
    url(r'^create$', views.create, name='create'),
    url(r'^addcomment', views.addcomment, name='addcomment'),
    url(r'^register$', views.register, name='register'),
    # # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    # url(r'^edit/(\d+)$', views.edit, name='edit'),
    url(r'^profile/(\w+)$', views.profile, name='profile'),
    url(r'^otherprofile/(\w+)$', views.otherprofile, name='otherprofile'),
    # url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^photo/(?P<id>\w+)$', views.get_photo, name='photo'),
    url(r'^get-list-json$', views.get_list_json),
    # url(r'^get-comment-list-json/?post_id=(\d+)$', views.get_comment_list_json),
    url(r'^get-list-xml$', views.get_list_xml),
    url(r'^get-comment-list-json$', views.get_comment_list_json),
    url(r'^get-list-xml-template$', views.get_list_xml_template),
    url(r'^get-follow-list-json$', views.get_follow_list_json),

]

