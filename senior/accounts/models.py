from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.validators import RegexValidator
import re

# 근우형 성공작

# class MyUserManager(BaseUserManager):
#     def create_user(self, email, username, is_mentor, password =None):
#         if not email:
#             raise ValueError('Need email')

#         user = self.model(
#             email = self.normalize_email(email),
#             username = self.username,
#             is_mentor = self.is_mentor
#             )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user


# class ProfileUser(AbstractBaseUser):
#     username = models.CharField(max_length=20, unique=True)
#     email = models.EmailField()
#     is_mentor = models.BooleanField()

#     objects = MyUserManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['is_mentor']

def phone_validator(value):
    number = ''.join(re.findall(r'\d+', value))
    return RegexValidator(r'^01[016789]\d{7,8}$', message= '번호를 입력해주세요')(number)



class PhoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 10)
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(phone_validator)

class Category(models.Model):
    title = models.CharField(max_length = 20)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    is_mentor = models.BooleanField()
    user_photo = models.ImageField(upload_to='%Y/%m/%d')
    category = models.ForeignKey(Category, blank = True)
    self_intro = models.TextField(max_length = 500)
    phone = PhoneField(blank = True)

    def __str__ (self):
        return self.user.username

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user, is_mentor =user.is_mentor, user_photo = user.user_photo, category = user.category, self_intro = user.self_intro, phone = user.phone)
        user_profile.save()

