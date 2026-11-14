import json
import os


class SettingsStore :
    def __init__(self, path: str):
        self.path = path
        self.data = {"widgets":{}} #no widgets to start with

    def load(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r") as file:
            self.data = json.load(file)

    def save(self):
        
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent = 3)

    def get_widget_ids(self):
        return list(self.data["widgets"].keys())

    def get_state(self, widget_id: str):
        return self.data["widgets"].get(widget_id)

    def set_state(self, widget_id: str, state: dict):
        self.data["widgets"][widget_id] = state
    