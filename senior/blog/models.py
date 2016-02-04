from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

def min_length_validator(value):
    if len(value) > 100:
        raise forms.ValidationError('100글자 이내로 입력하라고 !!!')

