from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from accounts.models import Profile
# Create your models here.

def min_length_validator(value):
    if len(value) > 100:
        raise forms.ValidationError('100글자 이내로 입력하라고 !!!')


class Question(models.Model):
    mentor = models.ForeignKey(Profile, related_name = "question_mentor", on_delete = models.CASCADE, limit_choices_to = {'is_mentor': True},)
    mentee = models.ForeignKey(Profile, related_name = "qustion_mentee",on_delete = models.CASCADE, limit_choices_to = {'is_mentor' : False})
    title = models.CharField(max_length = 30)
    message = models.TextField(max_length = 500)

    def __str__(self):
        return self.title

class Review(models.Model):
    mentee = models.ForeignKey(Profile, related_name = "review_mentee", on_delete = models.CASCADE, limit_choices_to = {'is_mentor': False})
    mentor = models.ForeignKey(Profile, related_name = "review_mentor", on_delete = models.CASCADE, limit_choices_to = {'is_mentor': True})
    message = models.TextField(max_length = 100)


class Notice(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Freeboard(models.Model):
    author = models.ForeignKey(Profile)
    title = models.CharField(max_length=50)
    content = models.TextField()
    auth = models.ForeignKey(Profile, related_name="Freeboard_auth")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    freeboard = models.ForeignKey(Freeboard)
    author = models.ForeignKey(Profile)
    message = models.TextField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title