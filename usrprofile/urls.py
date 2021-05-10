from django.conf.urls import url
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import user_profile_home, user_about, user_education, user_expreience, user_portfolio, \
    base_edit, edit_user_about, MyProfileUpdate, MyEducation, profile_education, MySkill, my_activity, MyProtfolio, \
    MyAddress, load_cities, myAddress, UserProfileHome, Git_Link, user_contact_info, send_email, I_AM, download_resume

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

app_name='user-profile'

urlpatterns=[

    # url(r'^profile-home/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
    #     cache_page(CACHE_TTL)(UserProfileHome.as_view()), name='edit-profile-home'),

    url(r'^profile-home/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        UserProfileHome.as_view(), name='edit-profile-home'),

    path('home' , user_profile_home , name='user-home'),

    path('about' , user_about , name='user-about'),




    path('education' ,user_education , name='user-education'),
    path('experience' , user_expreience , name='user-experience'),
    path('portfolio' , user_portfolio , name='user-portfolio'),

    path('git_linl', Git_Link, name='git_link'),

    path('send-email' , send_email , name='send-email'),

    path('user-contact-info' ,  user_contact_info , name='user-conatct-info'),



    path('base-edit', base_edit , name='base-edit' ),

    # url(r'^edit-user-about/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
    #     edit_user_about, name='edit-user-about'),

    url(r'^edit-user-about/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        MyProfileUpdate.as_view(), name='edit-user-about'),

    #
    # url(r'^edit-user-education/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
    #     profile_education, name='edit-user-edication'),

    url(r'^edit-user-education/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        MyEducation.as_view(), name='edit-user-edication'),

    url(r'^I-am/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        I_AM.as_view(), name='I-am'),

    url(r'^edit-user-skills/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        MySkill.as_view(), name='edit-user-skills'),

    # url(r'^edit-user-activity/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
    #     my_activity, name='edit-user-activity'),

    url(r'^edit-user-activity/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        MyProtfolio.as_view(), name='edit-user-activity'),

    url(r'^edit-user-address/(?P<user_id>[0-9A-Za-z_\-/]+)/$',
        myAddress.as_view(), name='edit-user-address'),

        path('ajax/load-cities/', load_cities, name='ajax_load_cities'),

    url(r'^upload-resume/(?P<user_id>[0-9A-Za-z_\-/]+)/$', download_resume.as_view(), name='upload-resume'),
    #




]