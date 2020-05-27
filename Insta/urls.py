"""instaDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from Insta.views import HelloWorld, PostsView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, addLike, UserDetailView, toggleFollow, EditUserView

urlpatterns = [
    path('', HelloWorld.as_view(), name = 'helloworld'),
    path('posts/', PostsView.as_view(), name = 'posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name = 'post_detail'),
    path('post/new/', PostCreateView.as_view(), name = 'make_post'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name = 'post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name = 'post_delete'),
    path('like/', addLike, name='addLike'),
    path('user/<int:pk>', UserDetailView.as_view(), name = 'user_detail'),
    path('togglefollow/', toggleFollow, name='togglefollow'),
    path('edit_profile/<int:pk>/', EditUserView.as_view(), name='edit_profile'),
]
