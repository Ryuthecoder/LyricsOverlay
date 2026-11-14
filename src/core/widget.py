import sys
import signal
from PyQt6.QtWidgets import QApplication
from core.settings_store import SettingsStore
from core.widget_manager import WidgetManager
from widgets.lyrics_widget import LyricsWidget


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)    # lets Ctrl+C quit the app
    app = QApplication(sys.argv)

    settings = SettingsStore("settings.json")
    settings.load()
    if not settings.get_widget_ids():               # first run: add the lyrics widget
        settings.set_state("lyrics", {"type": "lyrics", "x": 100, "y": 100, "always_on_top": True})

    manager = WidgetManager(settings, {"lyrics": LyricsWidget})
    manager.open_all()
    app.exec()


if __name__ == "__main__":
    main()