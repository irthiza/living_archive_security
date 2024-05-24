from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django_tables2 import SingleTableMixin


class PageHeaderMixin:
    page_title = None
    add_url = None
    list_url = None
    add_perms = None
    request = None
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) if hasattr(super(), 'get_context_data') else {}
        context['page_title'] = self.page_title
        content_type = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        if self.add_url and self.request.user.is_authenticated:
            context['add_link'] = self.add_url
        if self.list_url and self.request.user.has_perm(f'{content_type.app_label}.view_{content_type.model}'):
            context['list_link'] = self.list_url
        return context


class CustomSingleTableMixin(SingleTableMixin):
    request = None
    model = None
    detail_url = None
    edit_url = None
    delete_url = None

    def get_table_kwargs(self):
        ctx = super().get_table_kwargs()
        content_type = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        ctx['detail_url'] = self.detail_url
        ctx['view_perms'] = True  # Everyone can view
        ctx['edit_perms'] = True  # Everyone can see the edit button
        ctx['delete_perms'] = True  # Everyone can see the delete button
        ctx['edit_url'] = self.edit_url
        ctx['delete_url'] = self.delete_url
        return ctx

