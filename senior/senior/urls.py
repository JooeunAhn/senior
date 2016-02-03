"""senior URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'blog:index'),
    url(r'^notice/$', 'blog:notice_list'),
    url(r'^notice/(?P<pk>\d+)/$', 'blog:notice_detail'),
    url(r'^thanks/', 'blog.views.freeboard_list'),
    url(r'^thanks/(?P<pk>\d+)/$', 'blog:thanks_detail'),
    url(r'^freeboard/$', 'blog:freeboard_list'),
    url(r'^freeboard/(?P<pk>\d+)/$', 'blog:freeboard_detail'),
]
