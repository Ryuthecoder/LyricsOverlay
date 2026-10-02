import os

import requests 
from dotenv import load_dotenv

load_dotenv()

sp_dc = os.getenv("SP_DC")


url = "https://spotify.com"

spotify_cookie = {
    "sp_dc": sp_dc,
}

r = requests.get(url, cookies=spotify_cookie)

print(r.status_code) 
