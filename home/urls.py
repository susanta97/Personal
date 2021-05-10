from django.conf.urls import url
from django.urls import path
from django.views.decorators.cache import cache_page

from . views import *
# from .views import (
#     indexView,
#     postFriend,
#     checkNickName,
#     FriendView
# )
app_name='home'

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


urlpatterns = [
    # path('', home, name='home'),

    # path('' ,  cache_page(CACHE_TTL)(Home.as_view()) , name='home'),

    path('' ,  Home.as_view(), name='home'),

    url(r'^download-cv/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        download_cv, name='doenload_cv'),



    url(r'^/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        Home.as_view(), name='friend-details'),

    path('send-email', email_send, name='send-email'),

    path('post/ajax/model-auth', model_login, name = "model_login"),
]