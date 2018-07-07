from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from uiop import authentication_view
from . import channel_view
from . import file_view
from . import profiles_view
from . import priviledge_view
from . import Statistics_view


urlpatterns = [
    # url(r'^$', views.home, name='home'),

    # url(r'^register$', views.register, name='register'),
    # url(r'^login$', auth_views.login, {'template_name':'uiop/login.html'}, name='login'),
    # url(r'^logout$', auth_views.logout_then_login, name='logout'),

    url(r'^channel/(?P<code>\w+)$', channel_view.enter_channel, name='enter_channel'),
    url(r'^create-channel$', channel_view.create_channel, name='create_channel'),
    url(r'^login$', authentication_view.login, name='login'),
    url(r'^register$', authentication_view.register, name="register"),
    url(r'^download/(?P<id>\w+)$', file_view.download, name="download"),
    url(r'^modify-user-password$', profiles_view.modify_password, name="download"),
    url(r'^pull-new-file/(?P<code>\w+)$', channel_view.pull_new_file, name='pull_new_file'),
    url(r'^update-channel-info/(?P<code>\w+)$', channel_view.update_channel_info, name='update_channel_info'),
    url(r'^upload/(?P<code>\w+)$', file_view.upload, name="upload"),
    url(r'^modify-channel/(?P<code>\w+)$', priviledge_view.modify_channel, name="modify_channel"),
    url(r'^expire-now/(?P<code>\w+)$', priviledge_view.expire_now, name="expire_now"),
    # url(r'^online-user-in-channel/(?P<code>\d+)$', channel_view.online, name="online_user_in_a_channel"),
    url(r'^using-website/$', Statistics_view.peopleUsingWebsite, name="people_using_website"),
    url(r'^channels-day/$', Statistics_view.channelsDay, name="channel_in_a_day"),
    url(r'^average-file-info-channel/$', Statistics_view.averageChannel, name="average_file_info_channel"),
    url(r'^get-user-channel-list$', profiles_view.show_channel_list, name="show_channel_list"),
    url(r'^add-person/(?P<code>\w+)$', channel_view.add_person, name="add_person"),
    url(r'^minus-person/(?P<code>\w+)$', channel_view.minus_person, name="minus_person"),

]