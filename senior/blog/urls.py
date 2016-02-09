from django.conf.urls import url
from django.contrib import admin
from blog import views

urlpatterns =[
    url(r'^$', views.index, name = 'index'),
    url(r'^mentors/$', views.mentor_list, name = "mentor_list"),
    url(r'^mentors/(?P<pk>\d+)/$', views.mentor_detail, name = 'mentor_detail'),
    url(r'^questions/(?P<mentor_pk>\d+)/$', views.question_new, name = 'question_new'),
    url(r'^questions/views/$', views.question_list, name = 'question_list'),
    url(r'^questions/views/detail/(?P<pk>\d+)/$', views.question_detail, name = 'question_detail'),
    url(r'^questions/views/detail/(?P<pk>\d+)/edit/$', views.question_edit, name = "question_edit"),
    #url(r'^questions/views/detail/(?P<pk>\d+)/delete/$', views,question_delete, name = 'question_delete'),
    #url(r'^mentors/(?P<mentor_pk>\d+)/reviews//$', views.review_list, name = 'review_list'),
    url(r'^mentors/(?P<mentor_pk>\d+)/reviews/new/$', views.review_new, name = 'review_new'),
    url(r'^mentors/(?P<mentor_pk>\d+)/reviews/(?P<pk>\d+)/edit/$', views.review_edit, name = 'review_edit'),
    url(r'^notice/$', views.notice, name='notice'),
    url(r'^notice/new/$', views.notice_new, name='notice_new'),
    url(r'^notice/(?P<pk>\d+)/$', views.notice_detail, name = 'notice_detail'),
    url(r'^notice/(?P<pk>\d+)/edit/$', views.notice_edit, name = 'notice_edit'),
    url(r'^freeboard/$', views.freeboard, name ='freeboard'),
    url(r'^freeboard/new/$', views.freeboard_new, name ='freeboard_new'),
    url(r'^freeboard/(?P<pk>\d+)/$', views.freeboard_detail, name = 'freeboard_detail'),
    url(r'^freeboard/(?P<pk>\d+)/edit/$', views.freeboard_edit, name = 'freeboard_edit'),
    url(r'^freeboard/(?P<pk>\d+)/delete/$', views.freeboard_delete, name = 'freeboard_delete'),
    url(r'^freeboard/(?P<freeboard_pk>\d+)/comments/new/$', views.comment_new, name = 'comment_new'),
    url(r'^freeboard/(?P<freeboard_pk>\d+)/comments/(?P<pk>\d+)/edit', views.comment_edit, name = 'comment_edit'),
    url(r'^freeboard/(?P<freeboard_pk>\d+)/comments/(?P<pk>\d+)/delete', views.comment_delete, name = 'comment_delete'),
    url(r'^guide/$', views.guide, name='views.guide'),

    ]

