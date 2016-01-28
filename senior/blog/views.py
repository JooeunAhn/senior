from blog.models import Notice
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView


# Create your views here.

def index(request):
    return render(request, 'blog/index.html')


def notice_list(request):
    notice_list = Notice.objects.all()
    params = {'notice_list': notice_list}
    return render(request, 'blog/notice_list.html', params)



notice_detail = DetailView.as_view(model = Notice)