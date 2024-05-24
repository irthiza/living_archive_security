from .models import Blog
from .forms import BlogForm, PasscodeForm
from .tables import BlogTable

from django.contrib.auth import get_user_model
from ..helpers.utils import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from ..helpers.views import PageHeaderMixin, CustomSingleTableMixin
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View


User = get_user_model()

# class BlogPasscodeView(View):
#     template_name = 'blog/passcode.html'

#     def get(self, request, pk):
#         return render(request, self.template_name, {'pk': pk})

#     def post(self, request, pk):
#         passcode = request.POST.get('passcode')
#         blog = get_object_or_404(Blog, pk=pk)
#         if blog.passcode == passcode:
#             request.session[f'passcode_{pk}'] = passcode
#             return redirect('blog_detail', pk=pk)
#         else:
#             return render(request, self.template_name, {'pk': pk, 'error': 'Incorrect passcode'})


class BlogListView(LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, ListView):
    model = Blog
    template_name = 'multiple_select_list.html'
    permission_required = 'blog.view_blog'

    # PageHeaderMixin
    page_title = 'Blogs'
    add_perms = 'blog.add_blog'
    add_url = reverse_lazy('blog_add')

    # CustomSingleTableMixin
    table_class = BlogTable
    ordering = 'title'
    edit_url = 'blog_update'
    delete_url = 'blog_delete'
    detail_url = 'blog_detail'

    def get_queryset(self):
        return Blog.objects.filter(is_private=False)

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        kwargs['edit_perms'] = True  # Everyone can see the edit button
        kwargs['delete_perms'] = True  # Everyone can see the delete button
        kwargs['view_perms'] = True  # Everyone can view
        kwargs['edit_url'] = self.edit_url
        kwargs['delete_url'] = self.delete_url
        kwargs['detail_url'] = self.detail_url
        return kwargs

    
    

class BlogCreateViewGeneric( LoginRequiredMixin, PageHeaderMixin, CreateView):
    permission_required = 'blog.add_blog'
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog_list')
    page_title = 'blog'
    list_url = reverse_lazy('blog_list')

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author__user=user) | Blog.objects.filter(is_private=False)

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)
    

class BlogDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        if blog.is_private and blog.author.user != request.user:
            return render(request, 'blog_passcode.html', {'blog': blog, 'form': PasscodeForm()})
        return render(request, 'detail.html', {'blog': blog})

    def post(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        form = PasscodeForm(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data.get('passcode')
            if passcode == blog.passcode:
                return render(request, 'detail.html', {'blog': blog})
            else:
                return HttpResponseForbidden("Incorrect passcode")
        return render(request, 'blog_passcode.html', {'blog': blog, 'form': form})

class PrivateBlogListView(LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, ListView):
    model = Blog
    template_name = 'multiple_select_list.html'
    permission_required = 'blog.view_blog'

    # PageHeaderMixin
    page_title = 'Private Blogs'
    add_perms = 'blog.add_blog'
    add_url = reverse_lazy('blog_add')

    # CustomSingleTableMixin
    table_class = BlogTable
    ordering = 'title'
    edit_url = 'blog_update'
    delete_url = 'blog_delete'
    detail_url = 'blog_detail'


    def get_queryset(self):
        return Blog.objects.filter(is_private=True)
    
    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        kwargs['edit_perms'] = True  # Everyone can see the edit button
        kwargs['delete_perms'] = True  # Everyone can see the delete button
        kwargs['view_perms'] = True  # Everyone can view
        kwargs['edit_url'] = self.edit_url
        kwargs['delete_url'] = self.delete_url
        kwargs['detail_url'] = self.detail_url
        return kwargs


class BlogCreateViewGeneric(LoginRequiredMixin, PageHeaderMixin, CreateView):
    permission_required = 'blog.add_blog'
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog_list')
    page_title = 'blog'
    list_url = reverse_lazy('blog_list')

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author__user=user) | Blog.objects.filter(is_private=False)

    
    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    permission_required = 'blog.change_blog'
    model = Blog
    form_class = BlogForm 
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog_list')
    page_title = 'blog'
    list_url = reverse_lazy('blog_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        return obj

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class BlogDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    permission_required = 'blog.delete_blog'
    model = Blog
    template_name = 'delete.html'
    page_title = 'blog'
    success_url = reverse_lazy('blog_list')

    def get_success_url(self):
        if self.object.is_private:
            return reverse_lazy('private_blog_list')
        else:
            return reverse_lazy('blog_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author.user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this blog.")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/detail.html'

    def get_object(self, queryset=None):
        return self.request.user