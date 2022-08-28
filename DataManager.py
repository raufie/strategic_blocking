import json
import os


class DataManager:
    def __init__(self, path):
        self.path = path
        self.data = self.get_data_from_file(path)

    def get_data_from_file(self, path):
        try:
            f = open(os.path.join(path, "data.json"), "r")
            print(
                "\u001b[32mSUCCESS: Loaded data.json successfully\u001b[0m")
            return json.load(f)
        except Exception as e:
            print(
                "\u001b[33mERROR: Unable to open data.json successfully at given path\u001b[0m")
            print("creating new one")

            try:
                f = open(os.path.join(path, "data.json"), "w")
                json.dump([], f)
                return []
            except:
                print(
                    "\u001b[31mERROR: Unable to create new data.json successfully at given path\u001b[0m")
                exit()

    def add_data(self, data):
        self.data.append(data)

    def save(self):
        try:
            f = open(os.path.join(self.path, "data.json"), "w")
            json.dump(self.data, f, indent=6)
        except:
            print(
                "\u001b[31mERROR: Unable to save data.json successfully\u001b[0m")
            exit()

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
