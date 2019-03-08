# spotipy_collage 
Run server.py to get credentials. In your browser of choice, navigate to localhost:8081 , it will ask to authorize through Spotify, confirm and it should bring you to a JSON webpage of your information.
After this, simply run collage.py with a supplied full album, track, or playlist URI/URL.

To set this up, you will need Python 3, and you will need to run `pip install -r requirements.txt`

To run the lastfm_ripper, you will need an API key from lastfm. Once you have this, you can simply run it by typing in `python lastfm_ripper.py [user] [optional: period] [optional: limit]`
`period` can either be `overall, 7day, 1month, 3month, 6month, or 12month`
`limit` can be any number from 1 to 100, inclusive. 

Currently, when running `collage.py` you have to specify the first size of the collage image, by typing in `001.jpg` or `001.jfif`, depending on the format of the photo. You also need to specify the file format in the line, like so `python collage.py .jpg`. 

Canvas and collage size settings occur in `settings.json`, and any areas in the code that say `properties.json` have to be changed to `settings.json`. 
