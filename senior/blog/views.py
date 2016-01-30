from blog.models import Notice, FreeBoard
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView


# Create your views here.

def index(request):
    return render(request, 'blog/index.html')


def notice_list(request):
    notice_list = Notice.objects.all()
    params = {'notice_list': notice_list}
    return render(request, 'blog/notice_list.html', params)

def freeboard_list(request):
	freeboard_list = FreeBoard.objects.all()
	params = {'freeboard_list' : freeboard_list}
	return render(request, 'blog/freeboard_list.html', params)

def thanks_list(request):
	thanks_list = Thanks.objects.all()
	params = {'thanks_list' = thanks_list}
	return render(request, 'blog/thanks_list.html', params)


notice_detail = DetailView.as_view(model = Notice)
freeboard_detail = DetailView.as_view(models = FreeBoard)
thanks_detail = DetailView.as_view(models = Thanks)