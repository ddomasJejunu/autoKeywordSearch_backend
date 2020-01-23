from django.urls import path
from . import views

urlpatterns = [
    path('kakao/login/code/', views.kakaoGetCode, name='kakaoGetCode'),
    path('kakao/login/', views.kakaoLogin, name='kakaoLogin'),
    path('kakao/logout/', views.kakaoLogout, name='kakaoLogout'),
]