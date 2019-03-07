import json
import urllib3
import certifi
import urllib.request
import spotipy
import sys
import os

settings_file = open("properties.json")
settings_dict = json.load(settings_file)

API_KEY = settings_dict["LAST_FM_API_KEY"]

os.chdir("photos")

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
    rip_album_art(True)

def rip_album_art(outname=False):
    infile = open("lastfm.json")
    in_dict = json.load(infile)
    x = 0
    for item in in_dict["topalbums"]["album"]:
        x += 1
        img = item["image"][3]["#text"]
        artist = item["artist"]["name"]
        album_title = item["name"]
        if not outname:
            urllib.request.urlretrieve(img, artist + " - " + album_title + ".jpg")
            print("Saved under \"photos/" + artist + " - " + album_title + ".jpg\"")
        else:
            urllib.request.urlretrieve(img, str(x) + ".jpg")
            print("Saved under \"photos/" + str(x) + ".jpg\"")

            
if len(sys.argv) == 2:
    user_get_albums(sys.argv[1])


