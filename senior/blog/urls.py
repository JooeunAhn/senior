from django.conf.urls import url
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^mentors/$', views.mentor_list, name = "mentor_list"),
    url(r'^mentors/(?P<pk>\d+)/$', views.mentor_detail, name = 'mentor_detail'),
    url(r'^questions/(?P<mentor_pk>\d+)/$', views.question_new, name = 'question_new'),
    url(r'^questions/views$', views.question_list, name = 'question_list'),
    url(r'^questions/views/detail/(?P<pk>\d+)/$', views.question_detail, name = 'question_detail'),
    ]