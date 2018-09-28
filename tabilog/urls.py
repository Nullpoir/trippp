from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('post/',views.TabilogPost,name="TabilogPost"),
    path('post_done/',views.post_done,name="post_done"),
    path('',views.tabilog_list_show,name="tabilog_list_show"),
    path('articles/<int:number>',views.tabilog_show,name="tabilog_show"),
]
