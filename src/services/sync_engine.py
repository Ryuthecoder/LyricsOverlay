import time 
from PyQt6.qtCore import QObject, QTimer, pyqtSignal 
from services.spotify_service import get_access_token, get_current_song
from services.lyrics_service import fetch_lyrics



class SyncEngine(QObject):
    line_changed = pyqtSignal(str, str)
    no_lyrics = pyqtSignal(str)

    def __init__self(self):
        super().__init__()
        self.access_token = None
        self.song = None
        self.lyrics = []
        self.start_progress = 0
        self.start_time = 0
        self.last_line = None
        self.ticks = 0

        self.timer = QTimer() #I now use QTimer as Qt framework keeps its only track of time
        self.timer.timeout.connect(self.tick) #refactors legacy code of while loop with sleep

    def start(self):
        self.access_token = get_access_token()
        self.check_spotify()
        self.timer.start(100)

    def stop(self):
        self.timer.stop()

    def check_spotify(self):
        song = get_current_song(self.access_token)
        if song is None:
            self.song = None
            self.no_lyrics.emit("No song playing")
            return

        if (self.song is None) or (song["id"] != self.song["id"]):
            self.lyrics = fetch_lyrics(song)
            self.last_line = None
            if not self.lyrics: 
                self.no_lyrics.emit("No lyrics found")
                return

        self.song = song
        self.start_progress = self.song["progress_ms"]
        self.start_time = time.time()

    def tick(self):
        self.ticks += 1
        if self.ticks % 18000 == 0: #every 30 minutes new access token
            self.access_token = get_access_token()

        if self.song is None or not self.lyrics: #avoids errors)
            return

        progress = self.start_progress + ((time.time() - self.start_time)*1000)
        if not self.song["is_playing"]: # lyrics stay in case of pauses
            progress = self.start_progress

        current = ""
        next_line = None
        for line in self.lyrics:
            if line["time"] <= progress:
                current = line["text"]
            elif next_line is None:
                next_line = line["text"]

        if current != self.last_line:
            self.line_changed.emit((current, next_line or "") #if there is no next line, empty string is passed not None
            self.last_line = current)