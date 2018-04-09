from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'sign_in/$', views.sign_in, name='sign_in'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
    url(r'profile/view/$',
        views.user_profile_detail,
        name='user_profile_view'),
    url(r'profile/edit/$', views.user_profile, name='user_profile_edit'),
    url(
        r'profile/change_password/$',
        views.change_password,
        name='change_password'),
    url(r'profile/edit_avatar/$', views.edit_avatar, name='edit_avatar')
]
