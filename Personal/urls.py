"""Personal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from django.views.generic import TemplateView
from home.views import home

from django.views.static import serve
import re

urlpatterns = [
    path('account/', include('account.urls', namespace='account')),
    path('user/' , include('usrprofile.urls' , namespace='user-profile')),

    path('admin/', admin.site.urls),
    # path('' ,home , name='home')
    path('' , include('home.urls')),
    # path('' ,TemplateView.as_view(template_name='home.html',))
    path('accounts/', include('django.contrib.auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG == False:


if settings.STATIC_URL.startswith("/"):
    urlpatterns += [
        url(
            r'^{STATIC_URL}(?P<path>.*)$'.format(STATIC_URL=re.escape(settings.STATIC_URL.lstrip('/'))),
            serve,
            {'document_root': settings.STATIC_ROOT},
        ),
    ]





if settings.MEDIA_URL.startswith("/"):
    urlpatterns += [
        url(
            r'^{MEDIA_URL}(?P<path>.*)$'.format(MEDIA_URL=re.escape(settings.MEDIA_URL.lstrip('/'))),
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]