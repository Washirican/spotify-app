# --------------------------------------------------------------------------- #
# D. Rodriguez, 2020-10-16, File created.
# --------------------------------------------------------------------------- #
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='playlists-home'),
    path('about/', views.about, name='playlists-about'),
    path('login/', views.login, name='playlists-login'),

    ]
