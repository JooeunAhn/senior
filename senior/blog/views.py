from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from accounts.models import Profile
from blog.models import Question, Review, Notice, Freeboard
from blog.forms import QuestionForm, ReviewForm, NoticeForm, FreeboardForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')


def mentor_list(request):
    mentor_list = Profile.objects.filter(is_mentor = True)
    return render(request, 'blog/mentor_list.html', {'mentor_list' : mentor_list})


def mentor_detail(request, pk):
    mentor = Profile.objects.get(pk=pk)
    return render(request, 'blog/mentor_detail.html', {'mentor': mentor })


@login_required
def question_new(request,mentor_pk):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit = False)
            question.mentee = Profile.objects.get(user__username=str(request.user))
            question.mentor = get_object_or_404(Profile, pk = mentor_pk)
            question.save()
            messages.info(request, "새 질문 등록")
            return redirect('blog:mentor_list')
    else :
        form = QuestionForm()
    return render(request, 'blog/question_form.html', {'form':form})


@login_required
def question_list(request):
    user = Profile.objects.get(user = request.user)

    if user.is_mentor :
        questions = Question.objects.filter(mentor = user)
        return render(request, 'blog/question_list.html', {'question_list' : questions})
    else :
        questions = Question.objects.filter(mentee = user)
        return render(request, 'blog/question_list.html', {'question_list': questions})

def question_detail(request,pk):
    user = Profile.objects.get(user = request.user)

    if user.is_mentor:
        question = Question.objects.filter(mentor = user, pk = pk)
        return render(request, 'blog/question_detail.html', {"question": question},)
    else :
        question = Question.objects.filter(mentee = user, pk = pk)
        print (question)
        return render(request, 'blog/question_detail.html', {"question": question},)

#def review_list (request, mentor_pk):
#   review = Review.objects.filter(mentor = mentor_pk)
#  return render(request, 'blog/review_list.html', {'review_list' : review_list})

def review_new(request, mentor_pk):
    user = Profile.objects.get(user = request.user)
    if user.is_mentor :
        messages.info(request, "잘못된 접근입니다")
        return redirect('blog:mentor_detail', mentor_pk)
    else:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit = False)
                review.mentee = Profile.objects.get(user__username=str(request.user))
                review.mentor = get_object_or_404(Profile, pk = mentor_pk)
                review.save()
                messages.info(request, '리뷰를 등록했습니다.')
                return redirect('blog:mentor_detail', mentor_pk)
        else:
            form = ReviewForm()
        return render(request, 'blog/review_form.html', {'form': form})

def review_edit(request, mentor_pk, pk):
    review = Review.objects.get(pk = pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance = review)
        if form.is_valid():
            review = form.save(commit =False)
            review.mentee = Profile.objects.get(user__username = str(request.user))
            review.mentor = get_object_or_404(Profile, pk = mentor_pk)
            review.save()
            messages.info(request, '리뷰를 수정했습니다')
            return redirect('blog:mentor_detail', mentor_pk)
    else:
        form = ReviewForm()
    return render(request, 'blog/review_form.html', {'form':form,})


def notice(request):
    notice = Notice.objects.all()
    return render(request, 'blog/notice.html', {'notice':notice})


def notice_new(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NoticeForm(request.POST)
            if form.is_valid():
                notice = form.save()
                return redirect('blog:notice')
        else:
            form = NoticeForm()
        return render(request, 'blog/notice_form.html', {'form':form})
    else:
        messages.info(request, "잘못된경로임")
        return redirect('blog:index')


class NoticeDetailView(DetailView):
    def get_object(self, queryset=None):
        try:
            return Notice.objects.get(pk=self.kwargs['pk'])
        except Notice.DoesNotExist:
            raise Http404

        return get_object_or_404(Notice, pk=pk)

notice_detail = NoticeDetailView.as_view(model=Notice)


def notice_edit(request, pk):
    notice = Notice.objects.get(pk=pk)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NoticeForm(request.POST, instance=notice)
            if form.is_valid():
                notice=form.save()
                return redirect('blog:notice_detail', pk)
        else:
            form = NoticeForm(instance=notice)
        return render(request, 'blog/notice_form.html', {'form' : form,})


def freeboard(request):
    freeboard = Freeboard.objects.all()
    return render(request, 'blog/freeboard.html', {'freeboard':freeboard})


def freeboard_new(request):
    if request.method == 'POST':
        form = FreeboardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:freeboard')
    else:
        form = FreeboardForm()
    return render(request, 'blog/freeboard_form.html', {'form':form})


def freeboard_edit(request, pk):
    freeboard = Freeboard.objects.get(pk=pk)
    if request.method == 'POST':
        form = FreeboardForm(request.POST, instance=freeboard)
        if form.is_valid():
            freeboard = form.save()
            return redirect('blog:freeboard_detail', pk)
    else:
        form = FreeboardForm(instance=freeboard)
    return render(request, 'blog/freeboard_form.html', {'form':form})


class FreeboardDetailView(DetailView):
    def get_object(self, queryset=None):
        try:
            return Freeboard.objects.get(pk=self.kwargs['pk'])
        except Freeboard.DoesNotExist:
            raise Http404

        return get_object_or_404(Freeboard, pk=pk)

freeboard_detail = FreeboardDetailView.as_view(model=Freeboard)





