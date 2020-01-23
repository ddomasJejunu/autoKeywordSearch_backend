from django.urls import path
from . import views

urlpatterns = [
    path('kakao/request/login/', views.kakaoRequestLogin, name='kakaoRequestLogin'),
    path('kakao/login/', views.kakaoLogin, name='kakaoLogin'),
    path('kakao/logout/', views.kakaoLogout, name='kakaoLogout'),
]