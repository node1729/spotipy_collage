import spotipy
import os
import urllib3
import certifi
import urllib.request
import json
from PIL import Image
import sys

ID_LEN = 22

# get token
infile = open(".spotipyoauthcache")
in_dict = json.load(infile)
bearer_token = in_dict["access_token"]

os.chdir("./photos/")

def spotifyAPIReq(URL):
    http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where())

    r = http.request("GET", URL,
            headers={
                "Authorization": "Bearer " + bearer_token
                })
    output = json.loads(r.data.decode("utf-8"))
    return output

# save album artwork
def spot_album_save(album_id, outname=None):
    print("got album id: " + album_id)
    album_dict = spotifyAPIReq("https://api.spotify.com/v1/albums/" + album_id)
    outfile = open("album.json", "w")
    json.dump(album_dict, outfile, indent=4) 
    
    # set this variable to 0 for max size image (640x640), 1 is for 300x300, and 2 is for 64x64
    size = 2
    
    img = album_dict["images"][size]["url"]
    artist = album_dict["artists"][0]["name"]
    album_title = album_dict["name"]
    # if outname supplied, set that as the filename, useful for loops
    if not outname:
        urllib.request.urlretrieve(img, artist + " - " + album_title + ".jfif")
        print("Saved under \"photos/" + artist + " - " + album_title + ".jfif\"")
    else:
        urllib.request.urlretrieve(img, outname + ".jfif")
        print("Saved under \"photos/" + outname + ".jfif\"")
      
# get album from track
def spot_track_to_album(track_id):
    track_dict = spotifyAPIReq("https://api.spotify.com/v1/tracks/" + track_id)
    outfile = open("track.json", "w")
    json.dump(track_dict, outfile, indent=4)
    spot_album_save(track_dict["album"]["artists"][0]["id"])

# get tracks from playlist
def tracks_from_playlist(playlist_id):
    playlist_dict = spotifyAPIReq("https://api.spotify.com/v1/playlists/" + playlist_id)
    outfile = open("playlist.json", "w")
    json.dump(playlist_dict, outfile, indent=4)
    x = 1
    for item in playlist_dict["tracks"]["items"]:
        spot_album_save(item["track"]["album"]["uri"][-ID_LEN:], str(x))
        x += 1


if len(sys.argv) == 2:
    if "/album/" in sys.argv[1]:
        print("Saving album cover from command line")
        spot_album_save(sys.argv[1][sys.argv[1].index("/album/") + 7:sys.argv[1].index("/album/") + 7 + ID_LEN])
    elif "spotify:album:" in sys.argv[1]:
        print("Saving album cover from command line")
        spot_album_save(sys.argv[1][-ID_LEN:])
    elif "/track/" in sys.argv[1]:
        print("Attempting to find album cover from command line")
        spot_track_to_album(sys.argv[1][sys.argv[1].index("/track/") + 7:sys.argv[1].index("/track/") + 7 + ID_LEN])
    elif "spotify:track:" in sys.argv[1]:
        print("Attempting to find album cover from command line")
        spot_track_to_album(sys.argv[1][-ID_LEN:])
    elif "/playlist/" in sys.argv[1]:
        print("Dumping playlist json")
        tracks_from_playlist(sys.argv[1][sys.argv[1].index("/playlist/") + 10:sys.argv[1].index("/playlist/") + 10 + ID_LEN])
    elif ":playlist:" in sys.argv[1]:
        print("Getting tracks from playlist")
        tracks_from_playlist(sys.argv[1][-ID_LEN:])

