from django.urls import path
from .views import BlogListView,ProfileDetailView,BlogDetailView, PrivateBlogListView, BlogCreateViewGeneric, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('private_blogs/', PrivateBlogListView.as_view(), name='private_blog_list'),
    path('add/', BlogCreateViewGeneric.as_view(), name='blog_add'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),   
    path('details/', ProfileDetailView.as_view(), name='profile_detail'),

]
