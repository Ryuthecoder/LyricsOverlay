import requests 

def fetch_lyrics(song: dict):
    LRCLIB_url = "https://lrclib.net/api/get"
    params={
        "track_name" : song["song_name"],
        "artist_name" : song["artist_name"],
        "album_name" : song["album_name"],
        "duration" : round(song["duration_ms"]/1000) #LRCLIB duration is in seconds so we need to convert ms to seconds
    }

    LRCLIB_headers = {"User-Agent": "LyricsWidget"}

    lyrics_response = requests.get(LRCLIB_url, params=params, headers=LRCLIB_headers)

    unformatted_syncedLyrics = lyrics_response.json()["syncedLyrics"]

    return format_lyrics(unformatted_syncedLyrics)

def format_lyrics(unformatted_syncedLyrics: str):
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

    return lyrics