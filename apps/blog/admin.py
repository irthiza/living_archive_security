from django.contrib import admin
from .models import Blog

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = [ 'title', 'body','is_private','author','passcode']
    list_display =['title', 'body','is_private','author','passcode']

