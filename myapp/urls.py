from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.loginuser, name='login'),
    path('signup', views.signup, name='signup'),
    path('user', views.user_page, name='user_page'),
    path('logot', views.logoutuser, name='logout_user'),
    path('ai_recommendation/', views.ai_recommendation, name='ai_recommendation'),
]