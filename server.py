from bottle import route, run, request
import spotipy
from spotipy import oauth2
import json


# Change this to settings.json for personal use, or create properties.json
infile = open("properties.json")
settings_dict = json.load(infile)

PORT_NUMBER = 8081
SPOTIPY_CLIENT_ID = settings_dict["CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = settings_dict["CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = "http://localhost:8081"
SCOPE = "user-library-read"
CACHE = ".spotipyoauthcache"

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

@route("/")

def index():
    access_token = ""
    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token")
        access_token = token_info["access_token"]
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code")
            token_info - sp_oauth.get_access_token(code)
            access_token = token_info["access_token"]

    if access_token:
        print("getting user info")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host="", port=PORT_NUMBER)
