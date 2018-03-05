import json, os

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def read_json(filename):
    with open(filename) as f:
        return json.load(f)