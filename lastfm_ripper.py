import json
import urllib3
import certifi
import urllib.request
import spotipy

settings_file = open("properties.json")
settings_dict = json.load(settings_file)

API_KEY = settings_dict["LAST_FM_API_KEY"]

def lastfmAPIReq(URL):
    http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where())

    r = http.request("GET", "http://ws.audioscrobbler.com/2.0/" + URL + "&api_key=" + API_KEY + "&format=json")
    output = json.loads(r.data.decode("utf-8"))
    return output

def user_get_albums(user):
    output = lastfmAPIReq("?method=user.gettopalbums&user=" + user + "&period=1month")
    test_file = open("lastfm.json", "w")
    json.dump(output, test_file, indent=4)

user_get_albums("node1729")

