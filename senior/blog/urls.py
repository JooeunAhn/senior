from django.conf.urls import url
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^mentors/$', views.mentor_list, name = "mentor_list"),
    url(r'^mentor/(?P<pk>\d+)/$', views.mentor_detail, name = 'mentor_detail'),

    ]