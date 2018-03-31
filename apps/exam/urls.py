from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^add_plan$', views.add_plan),
    url(r'^add_trip/(?P<id>\d+)$', views.add_trip),
    url(r'^remove_trip/(?P<id>\d+)$', views.remove_trip),
    url(r'^users/(?P<id>\d+)$', views.show_itineraries)
]