from django import forms
from blog.models import Question, Review


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','message']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['message']
