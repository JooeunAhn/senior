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
    mentor = models.ForeignKey(Profile, related_name = "mentor", on_delete = models.CASCADE, limit_choices_to = {'is_mentor': True},)
    mentee = models.ForeignKey(Profile, related_name = "mentee",on_delete = models.CASCADE, limit_choices_to = {'is_mentor' : False})
    title = models.CharField(max_length = 30)
    message = models.TextField(max_length = 500)

    def __str__(self):
        return self.title





