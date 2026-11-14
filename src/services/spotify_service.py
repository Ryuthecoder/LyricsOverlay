import os 
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = os.getenv("REDIRECT_URL")
refresh_token = os.getenv("REFRESH_TOKEN")



def get_access_token():
    token_url = "https://accounts.spotify.com/api/token"
    credientials = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token,
        "redirect_uri" : redirect_url
        
    }

    access_token_request = requests.post(token_url, data=credientials, auth=(client_id,client_secret))
    token_data = access_token_request.json()
    access_token = token_data["access_token"]

    return access_token

def get_current_song(access_token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization" : "Bearer " + access_token
    }
    player_request = requests.get(url, headers=headers)
    if player_request.status_code != 200: #runs when no song
        return None
    
    data = player_request.json()
    item = data["item"]

    song = {
        "id" : item["id"], #necessary for when song changes 
        "song_name" : item["name"], #necessary for syncing with LRCLIb
        "artist_name" : item["artists"][0]["name"], #necessary for syncing with LRCLIb
        "album_name" : item["album"]["name"], #necessary for syncing with LRCLIb
        "duration_ms" : item["duration_ms"], #for LRCLIB (ms = miliseconds)
        
        "progress_ms" : data["progress_ms"], #for LRCLIB, progress in ms into the song
        "is_playing" : data["is_playing"] #for LRCLIB, paused or playing to stop or start lyrics
    }

    return song