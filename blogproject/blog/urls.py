from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/mine/', views.my_posts, name='my_posts'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
