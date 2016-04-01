from django.contrib import admin
from .models import Sitehits, Poll, Choice, Files, Chat
# Register your models here.

admin.site.register(Sitehits)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Files)
admin.site.register(Chat)