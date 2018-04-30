from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from . import *
import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response. 


#  Client Keys
CLIENT_ID = "d30709ce7c90422b8c033d6b2fcefd1e"
CLIENT_SECRET = "f18105e646c544679c97ca248ca89698"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://0.0.0.0:5000"
PORT = 8080
REDIRECT_URI = "{}/callback/q".format(CLIENT_SIDE_URL)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()
auth_data = {}
access_token = None
refresh_token = None


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

@irsystem.route("auth")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@irsystem.route("callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    global access_token
    access_token = response_data["access_token"]
    global refresh_token
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)
    
    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    auth_data = display_arr

    print(access_token)
    return redirect("")

@irsystem.route("getcode",methods=["POST"])
def getcode():
    global access_token
    global refresh_token
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    refreshdata = {"refresh_token":refresh_token,"grant_type":"refresh_token"}
    r = requests.post("https://accounts.spotify.com/api/token",data=refreshdata,headers=headers)
    print(type(r.content))
    access_token = json.loads(r.content)['access_token']
    return str(access_token)

@irsystem.route("getsong",methods=["POST"])
def getsong():
    global access_token
    global refresh_token    
    thedata = request.get_json()
    artist = thedata['artist'].replace(" ","%20")
    track = thedata['track'].replace(" ","%20")
    tok = getcode()
    headers = {"Authorization": "Bearer {}".format(tok)}
    q = "artist:"+artist+"%20"+"track:"+track+"&type=track&limit=1"
    url = "https://api.spotify.com/v1/search?q="+q
    print(url)
    r = requests.get(url,headers=headers)
    print(r.content)
    return json.dumps(r.content)
