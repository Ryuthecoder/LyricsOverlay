import sys
import json
from PyQt6.QtWidgets import QApplication
from core.widget_manager import WidgetManager
from core.settings_store import SettingsStore
from core.widget import Widget


def main() : 
    app = QApplication(sys.argv)
    settings = SettingsStore("test.json")
    settings.load()
    manager = WidgetManager(settings, {"test": Widget})

    w = Widget("test", always_on_top=True)
    a = Widget("test1", always_on_top=False)

    w.draw_content = lambda painter: None   
    w.load_state(settings.get_state(w.widget_id))
    w.moved.connect(manager._widget_moved)            # prints the position when dragged
    w.show()

    a.draw_content = lambda painter: None   
    a.load_state(settings.get_state(a.widget_id))
    a.moved.connect(manager._widget_moved)            # prints the position when dragged
    a.show()

    print(json.dumps(settings.data, indent=4))

    app.exec()

if __name__ == "__main__":
    main()
    
