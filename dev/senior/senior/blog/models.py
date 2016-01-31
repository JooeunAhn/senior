from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

def min_length_validator(value):
    if len(value) > 100:
        raise forms.ValidationError('100글자 이내로 입력하라고 !!!')


class Notice(models.Model):
    title = models.CharField(max_length=100,
            validators=[min_length_validator],
            help_text='포스팅 제목을 100자 이내로 써주세요.')
    content = models.TextField()
    # tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class FreeBoard(models.Model):
	title = models.CharField(max_length=100,
			validators=[min_length_validator],
			help_text='포스팅 제목을 100자 이내로 써주세요.')
	author = models.CharField(max_length=10)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)


class Thanks(models.Model):
    author = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    freeboard = models.ForeignKey(FreeBoard)
    message = models.TextField()

    def __str__(self):
        return self.message




class Mentor(models.Model):
    name = models.CharField(max_length = 20)
    photo = models.ImageField(blank = True)
    self_word = models.CharField(max_length = 100)
    content = models.ImageField(blank = True)

class Mentee(models.Model):
    name = models.CharField(max_length = 20)
    photo = models.ImageField(blank =True)
    self_word = models.CharField(max_length = 100)

class Question(models.Model):
    title = models.CharField(max_length = 30)
    content = models.CharField(max_length = 500)
    mentor = models.ManyToManyField(Mentor)
    mentee = models.ManyToManyField(mentee)

class review(models.Model):
    content = models.CharField(max_length = 140)
    question = models.OneToOneField(Question)

class reply(models.Model):
    content = models.CharField(max_length = 500)
    question = models.OneToOneField(Question)











