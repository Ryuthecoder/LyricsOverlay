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

print(sp_dc)
print(r.status_code) 
