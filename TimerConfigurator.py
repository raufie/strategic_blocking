import json
import os


class TimerConfigurator:
    def __init__(self, path):
        self.path = path
        self.data = self.get_data_from_file(path)

    def get_data_from_file(self, path):
        try:
            f = open(os.path.join(path, "config.json"), "r")
            print(
                "\u001b[32mSUCCESS: Loaded config.json successfully\u001b[0m")
            return json.load(f)
        except Exception as e:
            print(
                "\u001b[33mERROR: Unable to open config.json successfully at given path\u001b[0m")
            print("creating new one")

            try:
                f = open(os.path.join(path, "config.json"), "w")
                json.dump({
                    "path": ".",
                    "timer_config": {
                        "starter_time": 5.0*60,
                        "main_time": 30.0*60
                    }
                }, f, indent=6)
                return {
                    "path": ".",
                    "timer_config": {
                        "starter_time": 5.0,
                        "main_time": 30.0
                    }
                }
            except:
                print(
                    "\u001b[31mERROR: Unable to create new timerconfig.json successfully at given path\u001b[0m")
                exit()

    def save_configuration(self, data):
        self.data = data
        f = open(self.path, "w")
        json.dump(self.data, f, indent=6)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def to_list(self):
        return [self.data["timer_config"]["starter_time"], self.data["timer_config"]["main_time"]]
