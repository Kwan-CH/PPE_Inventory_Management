import json
import sys

new_table = {}

def loadTable(path: str):
    with open("./configs/" + path, "r") as f:
        return json.load(f)


sys.modules[__name__] = loadTable