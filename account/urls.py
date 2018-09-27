from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('mypage/<int:pk>/', views.UserDetail.as_view(), name='mypage'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
]
