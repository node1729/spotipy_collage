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

def user_get_albums(user, period, limit):
    output = lastfmAPIReq("?method=user.gettopalbums&user=" + user + "&period=" + period + "&limit=" + limit)
    test_file = open("lastfm.json", "w")
    json.dump(output, test_file, indent=4)
    test_file.close() # close file to prevent JSONDecodeError
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
            urllib.request.urlretrieve(img, str(x).zfill(3) + ".jpg")
            print("Saved under \"photos/" + str(x).zfill(3) + ".jpg\"")

    infile.close()
if len(sys.argv) == 1:
    print("Invalid syntax, please input at least " + sys.argv[0] + " [user] [period](optional, default=1month) [limit](optional, default=25)")

if len(sys.argv) > 1:
    period = "1month"
    limit = "25"
    period_array = ["7day", "1month", "3month", "6month", "12month", "overall"]
    try:
        period = sys.argv[2]
        if period not in period_array:
            raise PeriodInvalidError("Period not in {}, given".format(period_array))
    except IndexError:
        period = "1month"

    try:
        limit = sys.argv[3]
        if int(limit) > 100 or int(limit) < 1:
            raise LimitInvalidError("Limit invalid, given {}, 1 <= limit <= 100 expected".format(limit))
    except IndexError:
        limit = "25"

    user_get_albums(sys.argv[1], period, limit)






