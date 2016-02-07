from django.conf.urls import url
from django.contrib.auth.views import login, logout
from accounts import views
from accounts.forms import LoginForm


urlpatterns = [
    url(r'^signup/$', views.signup),
    url(r'^login/$', login, kwargs = {'authentication_form': LoginForm,}),
    url(r'^logout/$', logout, {'next_page': 'blog:index'}),
    url(r'^account_delete/$', views.account_delete),
    url(r'^mypage/$', views.profile,),
    url(r'^account_edit/$', views.account_edit,)
]


