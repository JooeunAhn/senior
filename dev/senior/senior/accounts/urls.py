from django.conf.urls import url
from django.contrib.auth.views import login
from accounts import views
from accounts.forms import LoginForm


urlpatterns = [
    url(r'^signup/$', views.signup),
    url(r'^login/$', login, kwargs = {'authentication_form': LoginForm,}),
    url(r'^profile/$', views.profile),
    url(r'^signup/confirm/(?P<uidb64>[a-zA-Z0-9/_-]+)/(?P<token>[0-9a-zA-Z]{1,13}-[0-9a-zA-Z]{1,20})/$', views.signup_confirm)
]
