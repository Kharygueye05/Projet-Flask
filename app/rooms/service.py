from app.data import load_data, save_data

ROOMS_FILE = 'rooms.json'

DEFAULT_ROOMS = [
    {"id": 1, "name": "301", "capacity": 30},
    {"id": 2, "name": "202", "capacity": 30},
    {"id": 3, "name": "604", "capacity": 50},
    {"id": 4, "name": "801", "capacity": 50},
    {"id": 5, "name": "501", "capacity": 20}
]

def _load_rooms():
    return load_data(ROOMS_FILE)

def _save_rooms(rooms):
    save_data(ROOMS_FILE, rooms)

def init_rooms():
    rooms = _load_rooms()
    if not rooms:
        _save_rooms(DEFAULT_ROOMS)

def list_rooms():
    return _load_rooms()

def get_room_by_id(room_id):
    rooms = _load_rooms()
    for r in rooms:
        if r['id'] == room_id:
            return r
    return None

def get_room_by_name(name):
    rooms = _load_rooms()
    for r in rooms:
        if r['name'] == name:
            return r
    return None

def add_room(name, capacity=30):
    rooms = _load_rooms()
    new_id = max([r['id'] for r in rooms], default=0) + 1
    room = {"id": new_id, "name": name, "capacity": capacity}
    rooms.append(room)
    _save_rooms(rooms)
    return room