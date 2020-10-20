# --------------------------------------------------------------------------- #
# D. Rodriguez, 2020-10-19, File created.
# --------------------------------------------------------------------------- #
from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='user_profile-home'),
    path('home/', views.home, name='user_profile-home'),
    path('about/', views.about, name='user_profile-about'),
    path('login/', views.login, name='user_profile-login'),
    path('profile/', views.profile, name='user_profile-profile'),
    path('callback/', views.callback, name='user_profile-callback'),

    ]
