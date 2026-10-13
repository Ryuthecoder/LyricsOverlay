import os

import requests 
from dotenv import load_dotenv

load_dotenv()

sp_dc = os.getenv("SP_DC")
client_id = os.getenv("CLIENT_ID")
redirect_url = os.getenv("REDIRECT_URL")

url = "https://open.spotify.com/api/token?reason=transport&productType=web_player"

spotify_cookie = {
    "sp_dc": sp_dc,
}

r = requests.get(url, cookies=spotify_cookie)

#LRCLIB request
api_url = "https://lrclib.net/api/search"
query_track = {
    "track_name" : "Payphone",
    "artist_name" : "Maroon 5",
    "album_name" : "Overexposed",
    "duration" : "37"
}

c = requests.get(api_url,params=query_track)

print(c.text)
print(sp_dc)
print(r.status_code) 
