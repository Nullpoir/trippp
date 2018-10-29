from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('image_post/',views.PostImageHandler,name="image_post"),
]
