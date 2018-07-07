from django.conf.urls import url
from jquery_todolist import views

urlpatterns =[
    url(r'^$', views.home),
    url(r'^add-item$', views.add_item),
    url(r'^delete-item/(?P<item_id>\d+)$', views.delete_item),
    url(r'^get-list-json$', views.get_list_json),
    url(r'^get-list-xml$', views.get_list_xml),
    url(r'^get-list-xml-template$', views.get_list_xml_template),
]
