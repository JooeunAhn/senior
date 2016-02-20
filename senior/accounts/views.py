# -*- encoding: utf-8 -*-
# -*- decoding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator as default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from accounts.forms import SignupForm, SignupForm2, User_Change_Form, Profile_Change_Form
from accounts.models import Profile, Category
from blog.models import Column, Reply


@login_required
def profile(request):
    if request.user.is_superuser:
        messages.info(request, "슈퍼유저는 프로필 ㄴㄴ")
        return render(request, 'blog/index.html')
    else:
        profile = Profile.objects.get(user=request.user)
        column_list = Column.objects.filter(author=profile)
        column_count = Column.objects.filter(author=profile).count()
        if profile.is_mentor:
            reply_count = Reply.objects.filter(question__mentor = profile).count()
            return render(request, 'accounts/profile_mentor.html', {'reply_count': reply_count, 'profile': profile, 'column_list': column_list, "column_count": column_count})
        else:
            reply_count = Reply.objects.filter(question__mentee = profile).count()
            return render(request, 'accounts/profile_mentee.html', {'profile': profile, 'reply_count': reply_count,})


@login_required
def account_delete(request):
    account = Profile.objects.get(user=request.user)
    if request.method == "POST":
        account.user.delete()
        messages.success(request, '삭제완료')
        return redirect("blog:index")
    return render(request, 'accounts/account_confirm_delete.html', {'account': account, })


@login_required
def account_edit(request):
    user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form1 = User_Change_Form(request.POST, instance = user.user)
        form2 = Profile_Change_Form(request.POST,request.FILES, instance = user)
        if form1.is_valid():
            if form2.is_valid():
                form1.save()
                form2.save()
                messages.info(request, '수정완료')
                return redirect('accounts:mypage')
    else:
        form1 = User_Change_Form(instance=user.user)
        form2 = Profile_Change_Form(instance = user)

    return render(request, 'accounts/signup_edit.html', {'form1': form1, 'form2': form2,})


def signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = SignupForm2(
                request.POST,
                request.FILES,
                initial={"user_photo": "default/default.png", "self_intro": "자기소개를 입력해주세요"})

            if form.is_valid():
                try:
                    user = form.save()
                except AttributeError:
                    form.category = None

                authenticated_user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'])
                auth_login(request, authenticated_user)
                # 회원가입 승인
                # backend_cls = get_backends()[0].__class__
                # backend_path = backend_cls.__module__ + '.' + backend_cls.__name__
                # user.backend = backend_path
                # auth_login(request, user)

                messages.info(request, '환영합니다')
                return redirect('blog:index')

                # 회원가입 시에, 이메일 승인
                # user = form.save(commit = False)
                # user.is_active = False ##user 에게 권한주는 것의 핵심
                # user.save()
                # send_signup_confirm_email(request, user)
                # return redirect(settings.LOGIN_URL)
        else:
            form = SignupForm2()
        return render(request, 'accounts/signup.html', {'form': form, })
    else:
        messages.info(request, "잘못된 접근입니다.")
        return redirect('blog:index')


def signup_confirm(request, uidb64, token):

    User = get_user_model()

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request, '인증확인')

        return redirect(settings.LOGIN_URL)
    else:
        messages.error(request, '잘못된경로임')
        return redirect(settings.LOGIN_URL)
