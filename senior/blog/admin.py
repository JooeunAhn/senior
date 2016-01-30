from django.contrib import admin
from blog.models import Notice


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_display_links = ['title']


admin.site.register(Notice, NoticeAdmin)



# Register your models here.
