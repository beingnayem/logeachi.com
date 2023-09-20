from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'blog_title']
    
@admin.register(Blog_Comment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment_text']