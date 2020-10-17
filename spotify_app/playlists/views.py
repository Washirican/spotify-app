from django.shortcuts import render
import requests
import json


# Create your views here.
def home(request):
    """Display player list."""
    context = {}
    return render(request, 'playlists/home.html', context)


def about(request):
    context = {}
    return render(request, 'playlists/about.html', context)


def login(request):
    base_url = 'https://accounts.spotify.com/authorize'
    my_client_id = '0d8eb54d39d24a2790635c6a952bff53'
    response_type = 'code'
    redirect_uri = 'http://localhost:5000/callback/'
    scope = 'user-read-private user-read-email'

    request_url = f'{base_url}?' \
                  f'client_id={my_client_id}&' \
                  f'response_type={response_type}&' \
                  f'redirect_uri={redirect_uri}&' \
                  f'scope={scope}' \


    response = requests.get(request_url)
    login_page = response.content.decode()

    print(login_page)

    context = {login_page}

    return render(request, 'playlists/login.html', context)

