"""trippp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from account.views import Top
import article.views as article_view
from django.core.cache import cache
import trippp.settings as conf
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/",include("account.urls")),
    path('', Top.as_view(), name='top'),
    path('company/',include("article.urls")),
    path('tinymce/', include('tinymce.urls')),
    path('docs/<int:pk>',article_view.doc_show_ws,name="trippp_doc_show"),
    path('tabilog/',include("tabilog.urls")),
    path('api/',include("api.urls")),
]
if conf.DEBUG:
    urlpatterns += static(conf.MEDIA_URL, document_root=conf.MEDIA_ROOT)
