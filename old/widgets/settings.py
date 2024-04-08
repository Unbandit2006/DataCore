import json
import os


class Settings:
    def __init__(self, theme, application, time=None, file=None):
        self._theme = theme
        self._application = application
        self._time = time
        self._json_file = file

        # All just _theme
        self.paddingTop = self._theme["paddingTop"]
        self.paddingRight = self._theme["paddingRight"]
        self.paddingLeft = self._theme["paddingLeft"]
        self.paddingBottom = self._theme["paddingBottom"]
        self.borderRadius = self._theme["borderRadius"]

        self.background = self._theme["background"]
        self.foreground = self._theme["foreground"]
        self.textColor = self._theme["textColor"]
        self.hoverForeground = self._theme["hoverForeground"]
        self.hoverText = self._theme["hoverText"]

        self.debugNormal = self._theme["debugNormal"]
        self.debugError = self._theme["debugError"]
        self.debugBackground = self._theme["debugBackground"]
        self.debugSuccess = self._theme["debugSuccess"]

        # All just _application
        self.width = self._application["width"]
        self.height = self._application["height"]
        self.fps = self._application["fps"]
        self.debugMode = self._application["debugMode"]

    @staticmethod
    def from_json_file(json_file):
        with open(json_file) as file:
            json_dict = json.load(file)
            return Settings(**json_dict, time=os.path.getmtime(json_file), file=json_file)
        
    def __repr__(self) -> str:
        return f"<Settings {self._time}>"
        
    def check_changes(self):
        if self._time != os.path.getmtime(self._json_file):
            self = self.from_json_file(self._json_file)
