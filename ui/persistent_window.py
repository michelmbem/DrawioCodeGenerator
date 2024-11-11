import json
import traceback

from os import path, makedirs


class PersistentWindow:

    def __init__(self, filename):
        self.filename = filename

    @property
    def config_path(self):
        return path.join(path.expanduser("~"), ".drawiocodegen")

    def load_settings(self):
        file_path = path.join(self.config_path, self.filename)
        if not path.exists(file_path): return

        try:
            with open(file_path, 'r') as config_file:
                settings = json.load(config_file)

            self.SetPosition((settings['position']['x'], settings['position']['y']))
            self.SetSize((settings['size']['width'], settings['size']['height']))
        except Exception as e:
            print(f"{self.__class__.__name__} - Something went wrong: {e}")
            traceback.print_exception(e)


    def save_settings(self):
        position, size = self.GetPosition(), self.GetSize()
        settings = {
            'position': {'x': position.x, 'y': position.y},
            'size': {'width': size.width, 'height': size.height},
        }

        try:
            if not path.exists(self.config_path):
                makedirs(self.config_path)

            file_path = path.join(self.config_path, self.filename)
            with open(file_path, 'w') as config_file:
                json.dump(settings, config_file, indent=4)
        except Exception as e:
            print(f"{self.__class__.__name__} - Something went wrong: {e}")
            traceback.print_exception(e)
