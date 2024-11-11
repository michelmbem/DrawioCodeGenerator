import json
import traceback

from os import path, makedirs


class PersistentWindow:

    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def point_to_dict(position):
        return {'x': position.x, 'y': position.y}

    @staticmethod
    def size_to_dict(size):
        return {'width': size.width, 'height': size.height}

    @staticmethod
    def rect_to_dict(rect):
        return {**PersistentWindow.point_to_dict(rect), **PersistentWindow.size_to_dict(rect)}

    @staticmethod
    def dict_to_point(d):
        return d['x'], d['y']

    @staticmethod
    def dict_to_size(d):
        return d['width'], d['height']

    @staticmethod
    def dict_to_rect(d):
        return *PersistentWindow.dict_to_point(d), *PersistentWindow.dict_to_size(d)

    @property
    def config_path(self):
        return path.join(path.expanduser("~"), ".drawiocodegen")

    def load_settings(self):
        file_path = path.join(self.config_path, self.filename)
        if not path.exists(file_path): return

        try:
            with open(file_path, 'r') as config_file:
                settings = json.load(config_file)

            self.SetPosition(self.dict_to_point(settings['position']))
            self.SetSize(self.dict_to_size(settings['size']))
        except Exception as e:
            print(f"{self.__class__.__name__} - Something went wrong: {e}")
            traceback.print_exception(e)


    def save_settings(self):
        settings = {
            'position': self.point_to_dict(self.GetPosition()),
            'size': self.size_to_dict(self.GetSize()),
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
