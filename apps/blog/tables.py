from .models import Blog
from ..helpers.tables import CustomTable
import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe

class BlogTable(CustomTable):
    selection = tables.CheckBoxColumn(accessor='pk', attrs={
        "th__input": {
            "onclick": "toggle(this)"
        },
        "td__input": {
            "class": "table-selection"
        }
    })

    title = tables.Column(empty_values=(), verbose_name='Title', orderable=False)
    is_private = tables.Column(empty_values=(), verbose_name='Is private', orderable=False)
    author = tables.Column(empty_values=(), verbose_name='Author', orderable=False)
    body = tables.Column(empty_values=(), verbose_name='Body', orderable=False)

    def render_body(self, value, record):
        if len(record.body) > 100:
            return record.body[:100] + '...'
        return value

    def render_action(self, record):
        url = []
        detail_url = reverse('blog_detail', args=[record.pk])
        url.append('<a href="%s" class="btn btn-sm btn-light-info"><i class="flaticon-eye"></i></a>' % detail_url)
        if record.author.user == self.request.user:
            if self.edit_url:
                edit_url = reverse(self.edit_url, args=[record.pk])
                url.append('<a href="%s" class="btn btn-sm btn-light-warning"><i class="flaticon-edit"></i></a>' % edit_url)
            if self.delete_url:
                del_url = reverse(self.delete_url, args=[record.pk])
                url.append('<a href="%s" class="btn btn-sm btn-light-danger"><i class="flaticon-delete"></i></a>' % del_url)
        return mark_safe(' '.join(url))

    class Meta:
        model = Blog
        template_name = "django_tables2/bootstrap4.html"
        fields = ('title', 'is_private', 'author', 'body')
        empty_text = 'There are no data yet'
        orderable = False
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        exclude = ('counter', )
        sequence = ('selection', 'title', 'is_private', 'author', 'body', 'action')
