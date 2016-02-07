from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from accounts.models import Profile
from blog.models import Question, Review
from blog.forms import QuestionForm, ReviewForm
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

