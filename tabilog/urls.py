from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('post/',views.TabilogPost,name="TabilogPost"),
    path('post_done/',views.post_done,name="post_done"),
    path('',views.tabilog_list_show,name="tabilog_list_show"),
    path('articles/<int:number>',views.tabilog_show,name="tabilog_show"),
    path('post_history/<int:user_pk>',views.post_history.as_view(),name="post_history"),
    path('edit/<int:user_pk>/<int:tabilog_pk>',views.tabilog_update,name="tabilog_update"),
    path('delete_confirm/<int:user_pk>/<int:tabilog_pk>',views.tabilog_pre_delete,name="tabilog_pre_delete"),
    path('delete/<int:user_pk>/<int:tabilog_pk>',views.tabilog_delete,name="tabilog_delete"),
]
