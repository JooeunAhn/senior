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

class Comment(models.Model):
    freeboard = models.ForeignKey(FreeBoard)
    message = models.TextField()

    def __str__(self):
        return self.message