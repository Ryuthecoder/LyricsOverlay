import os

import requests 
from dotenv import load_dotenv

load_dotenv()

sp_dc = os.getenv("SP_DC")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = os.getenv("REDIRECT_URL")
refresh_token = os.getenv("REFRESH_TOKEN")


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
    "grant_type" : "refresh_token",
    "refresh_token" : refresh_token,
    "redirect_uri" : redirect_url
    
}

r = requests.post(token_url, data=credientials, auth=(client_id,client_secret))

print(r.text)

token_data = r.json()
access_token = token_data["access_token"]

url = "https://api.spotify.com/v1/me/player/currently-playing"
headers = {
    "Authorization" : "Bearer " + access_token #Note: Spotify processes access token by splitting it on a space, so a missing space after Bearer will result in error
}

r = requests.get(url, headers=headers)
print(r.status_code)
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
