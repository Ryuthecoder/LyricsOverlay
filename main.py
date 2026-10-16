import os

import requests 
from dotenv import load_dotenv

load_dotenv()

sp_dc = os.getenv("SP_DC")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = os.getenv("REDIRECT_URL")


auth_url= "https://accounts.spotify.com/authorize"


spotify_cookie = {
    "client_id" : client_id,
    "response_type" : "code",
    "redirect_uri" : redirect_url,
    "scope" : "user-read-currently-playing",
}

r = requests.Request("GET",auth_url, params=spotify_cookie) #Assemble request
consent_url = r.prepare().url #Prepares the request to retrieve consent url for Spotify API access
print(consent_url)

token_url = "https://accounts.spotify.com/api/token"
credientials = {
    "grant_type" : "authorization_code",
    "code" : "AQAdM13EDHldQ6hRRLe86YVhlkDBCeljkUx7FgHqRtAffQEnV8TUUpWCPaVYzwi3KkaHcur2quPSR2v7cK447VWvS_hvSjovP-BCQtRwj5tLiGsUF5V2fxyNSmKPLD0fAwV9pmkZSOPsFLKv5fF6V9s0_W6Ngueu2-5pUxdm8xXLRj2p80Ct2Wjo2MH8KaS8ZpQ1gyTIe7XTvlFGrIE0tks1Dz9V78oLClz1M9Y3vlzQ9IJFXB5CnF4sjTlVxRHKppKmB6Wo",
    "redirect_uri" : redirect_url
}

r = requests.post(token_url, data=credientials, auth=(client_id,client_secret))

print(r.text)

#LRCLIB request
api_url = "https://lrclib.net/api/search"
query_track = {
    "track_name" : "Payphone",
    "artist_name" : "Maroon 5",
    "album_name" : "Overexposed",
    "duration" : "37"
}

c = requests.get(api_url,params=query_track)

# print(c.text)
# print(sp_dc)
# print(r.status_code) 
