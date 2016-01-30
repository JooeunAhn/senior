from blog.models import Notice, FreeBoard
from blog.forms import FreeBoardForm, CommentForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')

def notice_list(request):
    notice_list = Notice.objects.all()
    params = {'notice_list': notice_list}
    return render(request, 'blog/notice_list.html', params)

def freeboard_list(request):
	# 자유게시판 리스트
	freeboard_list = FreeBoard.objects.all()
	params = {'freeboard_list' : freeboard_list}
	return render(request, 'blog/freeboard_list.html', params)

def thanks_list(request):
	thanks_list = Thanks.objects.all()
	params = {'thanks_list' = thanks_list}
	return render(request, 'blog/thanks_list.html', params)


notice_detail = DetailView.as_view(model = Notice)
<<<<<<< HEAD
freeboard_detail = DetailView.as_view(models = FreeBoard)
thanks_detail = DetailView.as_view(models = Thanks)
=======
freeboard_detail = DetailView.as_view(model = FreeBoard)


def freeboard_new(request):
	# 자유게시판 글 추가
    if request.method == 'POST':
        form = FreeBoardForm(request.POST, requset.FILES)
        if form.is_valid():
            freebaord = form.save()
            return redirect('blog.views.freeboard_detail', freeboard.pk)
    else:
        form = FreeBoardForm()
    return render(request, 'blog/freeboard_form.html', {
        'form': form,
    })


def freeboard_edit(request, pk):
	# 자유게시판 글 수정
    freeboard = get_object_or_404(FreeBoard, pk=pk)
	if request.method == 'POST':
		form = FreeBoardForm(request.POST, instance=freeboard)
		if form.is_valid():
			freeboard = form.save()
            return redirect('blog.views.freeboard_detail', freeboard.pk)
    else:
        form = FreeBoardForm(instance=freeboard)
    return render(request, 'blog/freeboard_form.html', {
        'form': form,
    })


def comment_new(request, freeboard_pk):
    # 자유게시판 댓글 추가
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # comment.post = Post.objects.get(pk=post_pk)
            comment.post = get_object_or_404(FreeBoard, pk=freeboard_pk)
            comment.save()
            messages.info(request, '새로운 댓글을 등록했습니다.')
            return redirect('blog.views.freeboard_detail', freeboard_pk)
    else:
        form = CommentForm()    
    return render(request, 'blog/comment_form.html', {
        'form': form,
    })


def comment_edit(request, freeboard_pk, pk):
    # 자유게시판 댓글 수정 
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog.views.FreeBoard_detail', freeboard_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {
        'form': form,
        })
>>>>>>> origin/master
