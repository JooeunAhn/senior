from django import forms
from blog.models import Question, Review, Notice, Freeboard, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','message']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['message']


class NoticeForm(forms.ModelForm):
   class Meta:
      model = Notice
      fields = ['title', 'content']


class FreeboardForm(forms.ModelForm):
   class Meta:
      model = Freeboard
      fields = ['title', 'content']

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['message']