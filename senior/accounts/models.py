from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    is_mentor = models.BooleanField()


@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user, is_mentor =user.is_mentor)
        user_profile.save()
