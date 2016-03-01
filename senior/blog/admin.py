from django.contrib import admin
from .models import Sitehits, Poll, Choice
# Register your models here.

admin.site.register(Sitehits)
admin.site.register(Poll)
admin.site.register(Choice)