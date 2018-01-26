from django.conf.urls import url
from . import views
urlpatterns= [
    url(r'^travels/destination/(?P<travel_id>\d+)/join$', views.travel_join, name="travel_join" ),
    url(r'^travels/destination/(?P<travel_id>\d+)$', views.travel_desc, name="travel_desc" ),
    url(r'^travels/add_proc$', views.travel_add_proc ),
    url(r'^travels/add$', views.travel_add, name="travel_add"),
    url(r'^travels$', views.travels, name="travels"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^$', views.index),
]