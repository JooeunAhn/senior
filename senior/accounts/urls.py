from django.conf.urls import url
from django.contrib.auth.views import login, logout
from accounts import views
from accounts.forms import LoginForm


urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', login, kwargs={'authentication_form': LoginForm, }, name='login'),
    url(r'^logout/$', logout, {'next_page': 'blog:index'}, name='logout'),
    url(r'^account/delete/$', views.account_delete, name='account_delete'),
    url(r'^mypage/$', views.profile, name='mypage'),
    url(r'^account/edit/$', views.account_edit, name='account_edit')
]
