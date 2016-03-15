# -*- encoding: utf-8 -*-
from django import forms
from django.db import models
from accounts.models import Profile


def min_length_validator(value):
    if len(value) > 100:
        raise forms.ValidationError('100글자 이내로 입력하라고 !!!')

class Files(models.Model):
    file_name = models.FileField(upload_to='%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True, blank = True)
    
    def __str__(self):
        return file_name.name

class Sitehits(models.Model):
    hits = models.IntegerField(default=0)

    def __str__(self):
        return "사이트 조회수 : " + str(self.hits)

class Poll(models.Model):
    poll_content = models.CharField(max_length=200)
    poll_date = models.DateTimeField('게시된 날짜')

    def __str__(self):
        return self.poll_content

class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question.poll_content + " / " + self.choice_text

class Question(models.Model):
    mentor = models.ForeignKey(Profile, related_name="question_mentor", on_delete=models.CASCADE, limit_choices_to={'is_mentor': True},)
    mentee = models.ForeignKey(Profile, related_name="question_mentee", on_delete=models.CASCADE, limit_choices_to={'is_mentor': False})
    title = models.CharField(max_length=30)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, blank = True)
    updated_at = models.DateTimeField(auto_now=True, blank = True)

    def __str__(self):
        return self.title


class Review(models.Model):
    mentee = models.ForeignKey(Profile, related_name="review_mentee", on_delete=models.CASCADE, limit_choices_to={'is_mentor': False})
    mentor = models.ForeignKey(Profile, related_name="review_mentor", on_delete=models.CASCADE, limit_choices_to={'is_mentor': True})
    message = models.TextField(max_length=100)


class Notice(models.Model):
    category = models.CharField(max_length=8)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    freeboard = models.ForeignKey(Freeboard)
    author = models.ForeignKey(Profile)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Reply(models.Model):
    question = models.ForeignKey(Question, related_name="reply")
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)


class Column(models.Model):
    author = models.ForeignKey(Profile, limit_choices_to={"is_mentor": True})
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
