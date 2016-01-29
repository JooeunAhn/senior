from django import forms
from blog.models import FreeBoard, Comment


class FreeBoardForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['message']