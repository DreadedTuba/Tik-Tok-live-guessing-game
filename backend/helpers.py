import json

def get_data(file: str = "data") -> dict:
    """Grab json data from file"""
    store = dict()
    with open(f'{file}.json') as f:
        store = json.load(f)
    return store

def set_data(data: dict, file: str = "data") -> None:
    """Store data in json file"""
    with open(f'{file}.json', 'w') as f:
        json.dump(data, f, indent=4)