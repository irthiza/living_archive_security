import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe
import itertools


class CustomTable(tables.Table):
    action = tables.Column(empty_values=(), orderable=False, attrs={
        'th': {'class': 'text-center'},
        'td': {
            'width': lambda value: len(value.split('</a> ')) * 55,
            'class': 'text-center'
        }
    })
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)

    def __init__(self, *args, **kwargs):
        self.edit_perms = kwargs.pop('edit_perms', False)
        self.delete_perms = kwargs.pop('delete_perms', False)
        self.view_perms = kwargs.pop('view_perms', False)
        self.detail_url = kwargs.pop('detail_url', None)
        self.edit_url = kwargs.pop('edit_url', None)
        self.delete_url = kwargs.pop('delete_url', None)
        super().__init__(*args, **kwargs)

    def render_action(self, record):
        user = self.request.user
        url = []
        if self.view_perms and self.detail_url:
            detail_url = reverse(self.detail_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-info"><i class="flaticon-eye"></i></a>' % detail_url)
        if user == record.author.user and self.edit_perms and self.edit_url:
            edit_url = reverse(self.edit_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-warning"><i class="flaticon-edit"></i></a>' % edit_url)
        if user == record.author.user and self.delete_perms and self.delete_url:
            del_url = reverse(self.delete_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-danger"><i class="flaticon-delete"></i></a>' % del_url)
        return mark_safe(' '.join(url))

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
        return next(self.row_counter)
