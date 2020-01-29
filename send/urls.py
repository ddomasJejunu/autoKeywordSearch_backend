from django.urls import path
from . import views

urlpatterns = [
    path('kakao/push/', views.kakaoPush, name='push'),
    path('kakao/talk/me', views.kakaoSendToMe, name='sendToMe'),
]