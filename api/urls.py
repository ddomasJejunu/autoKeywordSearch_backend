from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('read/', views.search_list, name='read'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
]