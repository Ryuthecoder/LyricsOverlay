import os


import time
import requests 
from dotenv import load_dotenv

load_dotenv()

sp_dc = os.getenv("SP_DC")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = os.getenv("REDIRECT_URL")
refresh_token = os.getenv("REFRESH_TOKEN")

#============================
#OUTDATED: Since I already have refresh_token, I don't need to attain authorization_token using consent url anymore
#Spotify API Access (attaining consent url to retrieve authroization_token necessary for retrieving refresh_token)

auth_url= "https://accounts.spotify.com/authorize"


spotify_cookie = {
    "client_id" : client_id,
    "response_type" : "code",
    "redirect_uri" : redirect_url,
    "scope" : "user-read-currently-playing",
}

r = requests.Request("GET",auth_url, params=spotify_cookie) #Assemble request
consent_url = r.prepare().url #Prepares the request to retrieve consent url for Spotify API access
# print(consent_url)

#============================
#Continous loop that detects songs after songs
while True:

    #============================
    #Spotify API Access (attaining access_token using refresh_token)

    token_url = "https://accounts.spotify.com/api/token"
    credientials = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token,
        "redirect_uri" : redirect_url
        
    }

    r = requests.post(token_url, data=credientials, auth=(client_id,client_secret))

    # print(r.text)

    token_data = r.json()
    access_token = token_data["access_token"]

    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization" : "Bearer " + access_token #Note: Spotify processes access token by splitting it on a space, so a missing space after Bearer will result in error
    }

    player_request = requests.get(url, headers=headers)
    print("HTTP " + str(player_request.status_code))
    # print(player_request.text)

    #============================
    #Formatting Spotify Data for LRCLIB

    data = player_request.json()
    item = data["item"] #If I look at the output, I see that "item" is a key dictionary that holds all the relevant track information

    print(item["name"]) #prints the song title each time a new song starts

    song = {
        "id" : item["id"], #necessary for when song changes 
        "song_name" : item["name"], #necessary for syncing with LRCLIb
        "artist_name" : item["artists"][0]["name"], #necessary for syncing with LRCLIb
        "album_name" : item["album"]["name"], #necessary for syncing with LRCLIb
        "duration_ms" : item["duration_ms"], #for LRCLIB (ms = miliseconds)
        
        "progress_ms" : data["progress_ms"], #for LRCLIB, progress in ms into the song
        "is_playing" : data["is_playing"] #for LRCLIB, paused or playing to stop or start lyrics
    }

    # print(song)

    #=============================
    #Retrieving unformatted lyrics data from LRCLIB web api

    LRCLIB_url = "https://lrclib.net/api/get"
    LRCLIB_params = {
        "track_name" : song["song_name"],
        "artist_name" : song["artist_name"],
        "album_name" : song["album_name"],
        "duration" : round(song["duration_ms"]/1000) #LRCLIB duration is in seconds so we need to convert ms to seconds
    }
    LRCLIB_headers = {"User-Agent": "LyricsOverlay"} #LRCLIB requires which app (for me, it's this program) is contacting LRCLIB

    lyrics_response = requests.get(LRCLIB_url, params=LRCLIB_params, headers=LRCLIB_headers)
    lyrics_data = lyrics_response.json()
    unformatted_syncedLyrics = lyrics_data["syncedLyrics"]
    # print(lyricsData)
    # print(unformatted_syncedLyrics)
    # test = unformatted_syncedLyrics[5]
    # print(test)

    #=============================
    #Formatting unformatted lyrics  from LRCLIB web api
    lyrics = []
    for lyric in unformatted_syncedLyrics.splitlines():
        temp = lyric[1:]
        parts = temp.split("]",1)
        stamp = parts[0].split(":")
        text = parts[1]

        lyric_line = text.strip()

        minutes = stamp[0]
        seconds = stamp[1]

        int_minutes = int(minutes)
        float_seconds = float(seconds)
        time_ms = (int_minutes * 60 + float_seconds) * 1000

        lyrics.append({"time": time_ms, "text": lyric_line})

    # print(lyrics)
    # print(lyrics[0].get("time"))

    #=============================
    #Syncing Spotify live lryics with those of LRCLIB

    start_progress = song["progress_ms"] #fixes the error of misdetection by this program when song is already playing
    start_time = time.time()
    last_line = None


    while True:

        progress = start_progress + ((time.time() - start_time)*1000)

        current = ""
        for line in lyrics:
            if line["time"] <= progress:
                current = line["text"]

        if current != last_line:
            print(current)
            last_line = current

        if progress >= song["duration_ms"]:
            break

        time.sleep(0.1) #conserving computing resource
    
    
        

#=============================
#           Practice
#LRCLIB request practice 
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
