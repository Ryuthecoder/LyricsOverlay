from core.widget import Widget
from core.settings_store import SettingsStore

class WidgetManager: 
    def __init__(self, settings: SettingsStore, widget_types: dict[str, type[Widget]]):
        self.settings = settings
        self.widget_types = widget_types 
        self.widgets: dict[str, Widget] = {} #list of open widgets, none to start with


    def open_all(self):
        for widget_id in self.settings.get_widget_ids():
            self.open_widget(widget_id)


    def open_widget(self, widget_id: str):
        if widget_id in self.widgets:
            return #to signal already open

        state = self.settings.get_state(widget_id)
        type_name = state["type"]

        if type_name not in self.widget_types:
            print(f"Unknown Widget Type")
            return

        widget_class = self.widget_types[type_name]
        widget = widget_class(widget_id, state.get("always_on_top")) #Creates an object of the specific widget class (e.g. LyricsWidget)

        widget.load_state(state)
        widget.moved.connect(self._widget_moved) #signal is the movement and slot is _widget_move method
        widget.show()
        widget.start()

        self.widgets[widget_id] = widget #now detected as an open or active widget

    def close_widget(self, widget_id: str):
        if widget_id not in self.widgets:
            return

        widget = self.widgets.pop(widget_id) #java equivalent of removing and returning the value
        widget.stop()
        widget.close()

    def _widget_moved(self, widget_id: str, pos):
        state = self.settings.get_state(widget_id)
        state["x"] = pos.x()
        state["y"] = pos.y()
        self.settings.set_state(widget_id, state)
        self.settings.save() #settings.json is written
        