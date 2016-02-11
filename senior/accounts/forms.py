from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.models import Category
import re
from django.core.validators import RegexValidator
from django.shortcuts import redirect

def phone_validator(value):
    number = ''.join(re.findall(r'\d+', value))
    return RegexValidator(r'^01[016789]\d{7,8}$', message= '번호를 입력해주세요')(number)



def send_signup_confirm_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    context = {
    'user' : user,
    'host' : request.scheme + '://' + request.META['HTTP_HOST'],
    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
    'token' : token_generator.make_token(user),
     }

    subject = render_to_string('accounts/signup_confirm_subject.txt',context)
    body = render_to_string('accounts/signup_confirm_body.txt', context)
    to_email = [user.email]
    send_mail(subject, body, None, to_email, fail_silently=False)


class SignupForm(UserCreationForm):
    is_agree = forms.BooleanField(label ="약관동의",
        error_messages = {
            'required': '약관동의를 해주셔셔야 가입됩니다',
        })
    class Meta(UserCreationForm.Meta):
        #fields = ['username', 'email']
        fields = UserCreationForm.Meta.fields + ('email',) ##콤마 빠트리면 문자열이된다.
        ##장고 모델은 튜플이어야한다

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if email :
            User = get_user_model()
            if User.object.filter(email=email).exists():
                raise forms.ValidationError('중복된이메일')

        return email




class SignupForm2(UserCreationForm):
    email = forms.EmailField(required = False)
    #is_mentor = forms.ChoiceField(label = "멘토?멘티?",widget=forms.Select(),choices=OPTIONS,)
    is_mentor = forms.BooleanField(required = False)
    user_photo = forms.ImageField(required = False,)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required = False)
    self_intro = forms.CharField(widget=forms.Textarea, required = False)
    phone = forms.CharField(validators = [phone_validator])
    """
    def clean_photo(self):
        print (self['user_photo'].html_name)
        if not self['user_photo'].html_name in self.data:
            return self.fields['initial'].initial
        return self.cleaned_data['user_photo']
    """

    ### 이렇게하면 일단 DB에 저장은 안함 뒤에함수 호출 필요
    def save(self, commit=True):
        user = super(SignupForm2, self).save(commit=False)
        user.email = self.cleaned_data['email']   #### cleaned_data????
        user.is_mentor = self.cleaned_data['is_mentor']
        user.user_photo = self.cleaned_data['user_photo']
        user.category = self.cleaned_data['category']
        user.self_intro = self.cleaned_data['self_intro']
        user.phone = self.cleaned_data['phone']

        if commit:
            user.save()
        return user


# class SignupForm2(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = ProfileUser
#         fields = ['username','email','is_mentor']

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(SignupForm2, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


class LoginForm(AuthenticationForm):
    answer = forms.IntegerField(label = '3+3 = ?')

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', None)  ### 사전에서 key값이 없을경우 두번째값(None)을 넘겨라라는 뜻
        if answer != 6 :
            raise forms.ValidationError("땡")
        return answer

