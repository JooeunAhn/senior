from django import forms
from blog.models import Question, Review, Notice, Freeboard, Comment, Reply, Column


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','message']


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args,**kwargs)
        self.fields['message'].label=""

    class Meta:
        model = Review
        fields = ['message']
        widgets={'message':forms.TextInput(attrs={'class': 'form-control'})}


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
    widgets = {
      'message':forms.Textarea(attrs = {'style' : 'width : 100%; max_height : 20%', }),
    }


class ReplyForm(forms.ModelForm):
  class Meta:
    model = Reply
    fields = ['title', 'content']


class ColumnForm(forms.ModelForm):
  class Meta:
    model = Column
    fields = ['title', 'content']