from ..helpers.widgets import CustomSelect2Mixin
from .models import Blog


class BlogSelect2Widget(CustomSelect2Mixin):
    model = Blog
    queryset = Blog.objects.all().order_by('title')
    search_fields = ['title__icontains',]
