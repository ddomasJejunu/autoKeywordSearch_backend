from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogMain/', views.blogMain, name='blogMain'),
    path('blogMain/createBlog/', views.createBlog, name='createBlog'),
    path('blogMain/detail/<int:blog_id>/', views.detail, name='detail'),
    path('oauth/', views.oauth, name='oauth'),
]