from django.contrib import admin
from django.urls import path

from project_app import views


urlpatterns = [
    path("home/",views.homepage,name='homepage'),
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('list/', views.blog_list, name='blog_list'),
    path('create/', views.blog_create, name='blog_create'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('delete/<int:id>/', views.blog_delete, name='blog_delete'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),

]