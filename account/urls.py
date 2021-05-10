from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from account import views as core_views
from account.views import edit_account_view

app_name="accounts"

urlpatterns = [



    # url(r'^login/$', auth_views.LoginView.as_view(),name='login'),
    url('logout/', core_views.logout_view, name='logout'),
    url(r'^signup/$', core_views.register_view, name='signup'),

    url(r'^login/$', core_views.login_view, name='login'),

    # url(r'^login/$', auth_views.LoginView.as_view(),name='login'),

    # path('(?P<user_id>[0-9A-Za-z_\-]+)/edit/', edit_account_view, name="edit"),

    url(r'^edit/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        edit_account_view, name='edit'),


    # url(r'^profile/$', core_views.profile, name='profile'),
    # url(r'^profile/$', login_required(views.profile.as_view()), name='profile'),

    # url(r'^users/self/$', login_required(SelfUserDetailView.as_view()), name='users_self_detail'),

    # url(r'^users/$', core_views.UserDetailView, name='users_self_detail'),

    # url(r'^show/(?P<id>[0-9]{1,})/$', ProfileDetailView.as_view(), name='profile_detail'),
    # path(r'^show/?P<uuid>[0-9a-f\-]{32,}+?[a-f0-9]{4}+?4[a-f0-9]{3}+?[89ab][a-f0-9]{3}+?[a-f0-9]{12}/$', ProfileDetailView.as_view(), name='profile_detail'),
    # url(r'^show/(?P<uuid>[0-9a-zA-Z\-:_]+)/$',
    # login_required(ProfileDetailView.as_view()), name='profile_detail'),

    # url(r'^update/(?P<uuid>[0-9a-zA-Z\-:_]+)/$',
    # login_required(ProfileUpdateView.as_view()), name='profile-update'),
    #

    # url(r'^delete/(?P<uuid>[0-9a-zA-Z\-:_]+)/$',
    # login_required(ProfileDeleteView.as_view()), name='profile-delete'),




    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,130}-[0-9A-Za-z]{1,200})/$',
        core_views.activate, name='activate'),

    # url('ajax/validate_email/', views.validate_email, name='validate_username'),


]

