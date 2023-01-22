from appdata import AppDataPaths
import json

app_paths = AppDataPaths('strategic_blocker')

app_paths.setup()


def load_blocks_preset():
    obj = {}
    try:

        f = open(f"{app_paths.app_data_path}\\config.json", "r")
        s = f.read()
        if len(s) == 0:
            return []
        obj = json.loads(s)

    except:
        return []

    if 'preset' in obj.keys():
        return obj['preset']
    else:
        return [5, 25, 25]


def get_music():
    obj = {}
    try:
        f = open(f"{app_paths.app_data_path}\\config.json", "r")
        s = f.read()
        if s == "":
            return "NOT FOUND"
        obj = json.loads(s)
    except:
        return "NOT FOUND"

    if 'music' in obj.keys():
        return obj['music']
    else:
        return "NOT FOUND"


def save_preset(blocks):
    obj = {}
    f = ""
    try:
        f = open(f"{app_paths.app_data_path}\\config.json", "r")
        obj = json.loads(f.read())
    except:
        obj = {}
    obj['preset'] = list(blocks)
    f = open(f"{app_paths.app_data_path}\\config.json", "w")
    f.write(json.dumps(obj))


def save_music(music_path):
    obj = {}
    f = ""
    try:
        f = open(f"{app_paths.app_data_path}\\config.json", "r")
        obj = json.loads(f.read())
        print(obj)
    except:
        obj = {}
    obj['music'] = music_path
    f = open(f"{app_paths.app_data_path}\\config.json", "w")
    f.write(json.dumps(obj))


def add_categories(category):
    obj = {}
    f = ""
    try:
        f = open(f"{app_paths.app_data_path}\\config.json", "r")
        obj = json.loads(f.read())
    except:
        obj = {}

    if "categories" not in obj.keys():
        obj['categories'] = []
    print(category)
    obj['categories'].append(category)
    obj['categories'] = list(set(obj['categories']))
    f = open(f"{app_paths.app_data_path}\\config.json", "w")
    f.write(json.dumps(obj))


def get_categories():
    try:
        f = open(f"{app_paths.app_data_path}\\config.json", "r")
        s = f.read()
        if s == "":
            return []
        obj = json.loads(s)
    except:
        return []

    if 'categories' in obj.keys():
        return obj['categories']
    else:
        return ["NOT FOUND"]


def get_formatted(m):
    return f"{m//60}h{m%60}m"


def get_formatted_seconds(s):
    return f"{int(s)//3600}h{int(s)//60}m{int(int(s)%60)}s"
# def load_pip


def update_data():
    # append with the timestamp when the shit was done
    pass
