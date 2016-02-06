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
    return render(request, 'blog/mentor_detail.html', {'mentor': mentor})


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
        return redirect('blog:mentor_detail')
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

"""
@login_required
def comments_edit(request, post_pk,pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid() :
            comment =form.save(commit= False)
            comment.post = Post.get_object_or_404(pk = post_pk)
            comment.save()
            return redirect(comment.post)
    else:
        form = CommentForm(instance = comment)
    return render(request, 'blog/comment_form.html', {'form': form,})
"""



"""
@login_required
def comments_new(request, post_pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit= False)
            comment.author = request.user
            comment.post = get_object_or_404(Post,pk = post_pk)
            comment.save()
            ## 메세지 쓰는법 알아보기
            messages.debug(request, '새로운 댓글을 등록했습니다.')
            return redirect(comment.post) ## redirect comment.post
    else:
         form = CommentForm()
    return render(request,'blog/comment_form.html',{'form' : form})
"""


"""
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^mentors/$', views.mentor_list, name = "mentor_list"),
    url(r'^mentors/(?P<pk>\d+)/$', views.mentor_detail, name = 'mentor_detail'),
    url(r'^questions/(?P<mentor_pk>\d+)/$', views.question_new, name = 'question_new'),
    url(r'^questions/views$', views.question_list, name = 'question_list'),
    url(r'^questions/views/detail/(?P<pk>\d+)/$', views.question_detail, name = 'question_detail'),
    ]
"""

"""
def comments_new(request, post_pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit= False)
            comment.author = request.user
            comment.post = get_object_or_404(Post,pk = post_pk)
            comment.save()
            ## 메세지 쓰는법 알아보기
            messages.debug(request, '새로운 댓글을 등록했습니다.')
            return redirect(comment.post) ## redirect comment.post
    else:
         form = CommentForm()
    return render(request,'blog/comment_form.html',{'form' : form})
"""

"""
def signup(request):
    if request.method == 'POST':
        form = SignupForm2(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'])
            auth_login(request, authenticated_user)
            #회원가입 승인
            #backend_cls = get_backends()[0].__class__
            #backend_path = backend_cls.__module__ + '.' + backend_cls.__name__
            #user.backend = backend_path
            #auth_login(request, user)

            messages.info(request, '환영합니다')
            return redirect('blog:index')

            #회원가입 시에, 이메일 승인
            #user = form.save(commit = False)
            #user.is_active = False ##user 에게 권한주는 것의 핵심
            #user.save()
            #send_signup_confirm_email(request, user)
            #return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm2()
    return render(request, 'accounts/signup.html',
        {'form': form,})
"""
"""
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^mentors/$', views.mentor_list, name = "mentor_list"),
    url(r'^mentor/(?P<pk>\d+)/$', views.mentor_detail, name = 'mentor_detail'),

    ]
"""

