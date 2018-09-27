from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.biz_top, name='biz_top'),
    path('question/',views.question_get,name="question_get"),
    path('docs/<int:pk>/',views.doc_show,name="doc_show"),
    path("question_done/",views.q_done,name="q_done")
]
