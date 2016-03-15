from django import forms
from blog.models import Question, Review, Notice, Freeboard, Comment, Reply, Column
from blog.models import Files

class FileUploadForm(forms.ModelForm):

    class Meta:
        model = Files
        fields = "__all__" 

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "질문 제목을 입력하세요."
        self.fields['message'].label = "질문 내용을 입력하세요."

    class Meta:
        model = Question
        fields = ['title', 'message']


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = "멘토에게 남길 리뷰를 입력하세요."

    class Meta:
        model = Review
        fields = ['message']
        widgets = {'message': forms.TextInput(attrs={'class': 'form-control'})}


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']


class FreeboardForm(forms.ModelForm):
    class Meta:
        model = Freeboard
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = "댓글 내용을 입력하세요."

    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'class': 'form-control', }),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['title', 'content']


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title', 'content']
