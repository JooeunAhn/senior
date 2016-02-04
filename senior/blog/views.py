from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')



