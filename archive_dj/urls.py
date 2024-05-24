from django.contrib import admin
from django.urls import path, include
from allauth.account import views as auth_views
from apps.blog.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('blogs/', include('apps.blog.urls')),
     path("signup/", auth_views.login, name="account_signup"),
     path("login/", auth_views.login, name="account_login"),
    path("logout/", auth_views.logout, name="account_logout"),
]
