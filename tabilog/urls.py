from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    #path('', views.biz_top, name='biz_top'),
    path('post/',views.TabilogPost,name="TabilogPost"),
    path('post_done/',views.post_done,name="post_done"),
    #path('tabilog/<int:pk>/',views.doc_show,name="doc_show"),
]
