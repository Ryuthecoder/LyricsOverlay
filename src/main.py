import sys
import signal
from PyQt6.QtWidgets import QApplication
from core.settings_store import SettingsStore
from core.widget_manager import WidgetManager
from core.widget import Widget
from widgets.lyrics_widget import LyricsWidget


def main():
    app = QApplication(sys.argv)

    settings = SettingsStore("settings.json")
    settings.load()
    if not settings.get_widget_ids():               # (first run) add the lyrics widget
        settings.set_state("lyrics1", {"type": "lyrics", "x": 100, "y": 100, "always_on_top": True})
        # settings.set_state("lyrics2", {"type": "lyrics", "x": 100, "y": 100, "always_on_top": False})

    dict = {
        "lyrics": LyricsWidget,

    }
    manager = WidgetManager(settings, dict)
    manager.open_all()
    app.exec()


if __name__ == "__main__":
    main()