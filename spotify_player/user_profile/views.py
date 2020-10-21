from django.shortcuts import render, redirect
from urllib.parse import quote
import requests
import json
import pprint

#  Client Keys
CLIENT_ID = '0d8eb54d39d24a2790635c6a952bff53'
CLIENT_SECRET = 'cc9cc3d621744067a38fd7e30ab2ae38'

# Spotify URLS
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
SPOTIFY_API_URL = f'{SPOTIFY_API_BASE_URL}/{API_VERSION}'

# Server-side Parameters
CLIENT_SIDE_URL = 'http://127.0.0.1'
# CLIENT_SIDE_URL = 'https://washirican-spotify-app.herokuapp.com/'

PORT = 8000
REDIRECT_URI = f'{CLIENT_SIDE_URL}:{PORT}/callback/'
SCOPE = 'playlist-modify-public playlist-modify-private'
STATE = ''
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    'response_type': 'code',
    'redirect_uri': REDIRECT_URI,
    'scope': SCOPE,
    # 'state': STATE,
    # 'show_dialog': SHOW_DIALOG_str,
    'client_id': CLIENT_ID
    }


# Create your views here.
def home(request):
    print('\n===========================================================')
    print(f'Request Content from home View: {request}')
    print('===========================================================\n')

    return render(request, 'user_profile/home.html')


def about(request):
    print('\n===========================================================')
    print(f'Request Content from about View: {request}')
    print('===========================================================\n')

    return render(request, 'user_profile/about.html')


def profile(request):
    print('\n===========================================================')
    print(f'Request Content from profile View: {request}')
    print('===========================================================\n')

    # access_token = request.GET['token']
    #
    # authorization_header = {'Authorization': f'Bearer {access_token}'}
    #
    # print('\n===========================================================')
    # print(f'Token from profile View: {token}')
    # print('===========================================================\n')

    return render(request, 'user_profile/profile.html')


def login(request):
    print('\n===========================================================')
    print(f'Request Content from login View: {request}')
    print('===========================================================\n')

    # Auth Step 1: Authorization
    url_args = '&'.join(['{}={}'.format(key, quote(val)) for key, val in
                         auth_query_parameters.items()])

    auth_url = f'{SPOTIFY_AUTH_URL}/?{url_args}'

    print('\n===========================================================')
    print(f'Authorization URL from login View: {auth_url}')
    print('===========================================================\n')

    return redirect(auth_url)


def callback(request):
    print('\n===========================================================')
    print(f'Request Content fom callback View: {request}')
    print('===========================================================\n')

    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.GET['code']
    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    print('\n===========================================================')
    print(f'Post Request Response fom callback View: {post_request}')
    print('===========================================================\n')

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    token_type = response_data['token_type']
    expires_in = response_data['expires_in']

    print('\n===========================================================')
    print(f'Access Token from callback View: {access_token}')
    print('===========================================================\n')

    # =========================================================================
    # Moved to profile view.
    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {'Authorization': f'Bearer {access_token}'}

    print('\n===========================================================')
    print(f'Authorization Header from callback View: {authorization_header}')
    print('===========================================================\n')

    # Get profile data
    user_profile_api_endpoint = f'{SPOTIFY_API_URL}/me'
    profile_response = requests.get(user_profile_api_endpoint,
                                    headers=authorization_header)
    profile_data = json.loads(profile_response.text)
    #
    # # Get user playlist data
    # # playlist_api_endpoint = f'{profile_data['href']}/playlists'
    # # playlists_response = requests.get(playlist_api_endpoint,
    # #                                   headers=authorization_header)
    # # playlist_data = json.loads(playlists_response.text)
    #
    # # Combine profile and playlist data to display
    display_arr = [profile_data][0]  # + playlist_data['items']
    # # return render_template('index.html', sorted_array=display_arr)

    print('\n===========================================================')
    pprint.pprint(f'Profile Data from callback View:\n {display_arr}')
    print('===========================================================\n')

    context = {
        'display_arr': display_arr
        }
    # =========================================================================

    # TODO (D. Rodriguez 2020-10-19): After getting access token pass it to
    #  another function to get profile, playlists etc. Can this be done?

    return render(request, 'user_profile/profile.html', context)
    # return render(request, 'user_profile/callback.html', context)
    # return redirect('user_profile/profile.html')
    # return redirect('http://127.0.0.1:8000/profile/', token=access_token)
