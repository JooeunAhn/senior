from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from accounts.models import Profile
from blog.models import Question, Review, Notice, Freeboard, Comment
from blog.forms import QuestionForm, ReviewForm, NoticeForm, FreeboardForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re

# Create your views here.
reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)


# is it ok to do this in views.py?
#def process_request(request):
#    mobileuser = False
#    #if request.META.has_key('HTTP_USER_AGENT'):
#    user_agent = request.META['HTTP_USER_AGENT']
#    b = reg_b.search(user_agent)
#    v = reg_v.search(user_agent[0:4])
#    if b or v:
##        mobileuser = True
 #   else:
#        mobileuser = False
 #   return render(request, 'blog/index.html')

def owner_required_freeboard(model_cls, user_field_name = 'author'):

    def wrap(fn):
        def inner_wrap(request, *args, **kwargs):
            #print (getattr(request.instance, user_field_name))
            request.instance = get_object_or_404(model_cls, pk=kwargs['pk'])
            """
            삽질의 결과 ㅋㅋㅋㅋ 우리 팀원 모두 값 찍어보고 실행하시길!
            print(request.instance)
            print(type(request.instance))
            print(type(request.instance.author.user))
            print(type(request.user))
            print(request.instance.author.user)
            print(request.user)
            """
            if request.instance.author.user != request.user:
                ##if getattr(request.instance.author, user_field_name) != request.user:
                return HttpResponseForbidden('작성자만 가능합니다')
            return fn(request, *args, **kwargs)
        return inner_wrap
    return wrap



def index(request):
    return render(request, 'blog/index.html')


def mentor_list(request):

    mentor_list = Profile.objects.filter(is_mentor = True)
    paginator = Paginator(mentor_list, 10)
    page = request.GET.get('page')
    try:
        mentor_list = paginator.page(page)
    except PageNotAnInteger:
        mentor_list = paginator.page(1)
    except EmptyPage:
        mentor_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/mentor_list.html', {'mentor_list' : mentor_list})


def mentor_detail(request, pk):
    mentor = Profile.objects.get(pk=pk)
    return render(request, 'blog/mentor_detail.html', {'mentor': mentor, 'review_form': ReviewForm()})


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

@login_required
def question_detail(request,pk):
    user = Profile.objects.get(user = request.user)

    if user.is_mentor:
        question = Question.objects.filter(mentor = user, pk = pk)
        return render(request, 'blog/question_detail.html', {"question": question},)
    else :
        question = Question.objects.filter(mentee = user, pk = pk)
        return render(request, 'blog/question_detail.html', {"question": question},)

@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk = pk)
    if question.mentee.user != request.user:
        messages.warning(request, "권한이 없습니다")
        return redirect("blog:quesetion_list")
    else:
        if request.method == "POST":
            question.delete()
            messages.success(request, '삭제완료')
            return redirect("blog:question_list")
        return render(request, 'blog/question_confirm_delete.html', {'quesiton' : question ,})




#def review_list (request, mentor_pk):
#   review = Review.objects.filter(mentor = mentor_pk)
#  return render(request, 'blog/review_list.html', {'review_list' : review_list})
@login_required
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
@login_required
def review_edit(request, mentor_pk, pk):
    review = Review.objects.get(pk = pk)

    if review.mentee.user != request.user:
        messages.warning(request, "작성자가 아닙니다")
        redirect("blog:mentor_detail", mentor_pk)
    else:
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
            form = ReviewForm(instance = review)
        return render(request, 'blog/review_form.html', {'form':form,})

@login_required
def review_delete(request, mentor_pk, pk):
    review = get_object_or_404(Review, pk = pk)

    if review.mentee.user != request.user:
        messages.warning(request, "권한이 없습니다")
        return redirect("blog:review_list")
    else:
        if request.method == "POST":
            review.delete()
            messages.success(request, '삭제완료')
            return redirect("blog:mentor_detail", mentor_pk)
        return render(request, 'blog/review_confirm_delete.html', {'review':review,})




def notice(request):
    notice_list = Notice.objects.all()
    paginator = Paginator(notice_list, 10)
    page = request.GET.get('page')
    try:
        notice = paginator.page(page)
    except PageNotAnInteger:
        notice = paginator.page(1)
    except EmptyPage:
        notice = paginator.page(paginator.num_pages)

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


@login_required
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
    else:
        messages.info(request, "잘못된 접근입니다")
        return redirect("blog:index")


def freeboard(request):
    freeboard_list = Freeboard.objects.all()
    paginator = Paginator(freeboard_list, 10)
    page = request.GET.get('page')
    try:
        freeboard = paginator.page(page)
    except PageNotAnInteger:
        freeboard = paginator.page(1)
    except EmptyPage:
        freeboard = paginator.page(paginator.num_pages)

    context = {
    'freeboard' : freeboard,
    }
    return render(request, 'blog/freeboard.html', context)

@login_required
def freeboard_new(request):
    if request.method == 'POST':
        form = FreeboardForm(request.POST)
        if form.is_valid():
            freeboard = form.save(commit = False)
            freeboard.author = Profile.objects.get(user = request.user)
            freeboard.save()
            return redirect('blog:freeboard')
    else:
        form = FreeboardForm()
    return render(request, 'blog/freeboard_form.html', {'form':form})


@login_required
@owner_required_freeboard(Freeboard, 'author')
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


def freeboard_detail(request, pk):
    freeboard = get_object_or_404(Freeboard, pk=pk)
    return render(request, 'blog/freeboard_detail.html', {
        'freeboard': freeboard,
        'comment_form': CommentForm(),
     })

"""
김지은 detailview
class FreeboardDetailView(DetailView):
    def get_object(self, queryset=None):
        try:
            return Freeboard.objects.get(pk=self.kwargs['pk'])
        except Freeboard.DoesNotExist:
            raise Http404

        return get_object_or_404(Freeboard, pk=pk)

freeboard_detail = FreeboardDetailView.as_view(model=Freeboard)
"""

def guide(request):
    return render(request, 'blog/guide.html')


@login_required
@owner_required_freeboard(Freeboard, 'author')
def freeboard_delete(request, pk):
    freeboard = get_object_or_404(Freeboard, pk = pk)
    if request.method == "POST":
        freeboard.delete()
        messages.success(request, '삭제완료')
        return redirect("blog:freeboard")
    return render(request, 'blog/freeboard_confirm_delete.html', {'freeboard':freeboard})

@login_required
def comment_new(request, freeboard_pk):
    freeboard = get_object_or_404(Freeboard, pk = freeboard_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.freeboard = freeboard
            comment.author = Profile.objects.get(user=request.user)
            comment.save()
            return redirect('blog:freeboard_detail', freeboard_pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {"form":form})

@login_required
def comment_edit(request,freeboard_pk,pk):
    comment = get_object_or_404(Comment, pk = pk)

    if comment.author.user != request.user:
        messages.warning(request, "권한이 없습니다")
        return redirect("blog:freeboard_detail", freeboard_pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            form.save()
            messages.success(request, "수정완료!")
            return redirect("blog:freeboard_detail", freeboard_pk)
    else:
        form = CommentForm(instance = comment)

    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_delete(request,freeboard_pk,pk):
    comment = get_object_or_404(Comment, pk = pk)

    if comment.author.user != request.user:
        messages.warning(request, "권한이 없습니다")
        return redirect("blog:freeboard_detail", freeboard_pk)

    if request.method == "POST":
        comment.delete()
        messages.success(request, '삭제완료')
        return redirect("blog:freeboard_detail", freeboard_pk)
    return render(request, 'blog/comment_confirm_delete.html', {'comment':comment,})


@login_required
def question_edit(request, pk):
    user = Profile.objects.get(user = request.user)
    question = Question.objects.get(pk = pk)

    if question.mentee != user:
        messages.warning(request, "작성자가 아닙니다.")
        return redirect("blog:question_detail", pk)
    else:
        if user.is_mentor :
            messages.warning(request, "권한이 없습니다")
            return redirect("blog:question_detail", pk)
        else:
            if request.method == "POST":
                form = QuestionForm(request.POST, instance = question)
                if form.is_valid():
                    form.save()
                    messages.success(request, "질문이 수정되었습니다")
                    return redirect("blog:question_detail", pk)
            else:
                form = QuestionForm(instance = question)
            return render(request, 'blog/question_form.html', {'form':form})