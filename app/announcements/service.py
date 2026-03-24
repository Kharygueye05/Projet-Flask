from datetime import datetime
from app.data import load_data, save_data

ANNOUNCEMENTS_FILE = 'announcements.json'

def _load_announcements():
    return load_data(ANNOUNCEMENTS_FILE)


def _save_announcements(announcements):
    save_data(ANNOUNCEMENTS_FILE, announcements)


def list_announcements():
    announcements = _load_announcements()
    return sorted(announcements, key=lambda x: x['created_at'], reverse=True)


def add_announcement(title, content, author):
    announcements = _load_announcements()
    new_id = max([a['id'] for a in announcements], default=0) + 1
    announcement = {
        'id': new_id,
        'title': title,
        'content': content,
        'author': author,
        'created_at': datetime.now().isoformat()
    }
    announcements.append(announcement)
    _save_announcements(announcements)
    return announcement


def delete_announcement(announcement_id):
    announcements = _load_announcements()
    announcements = [a for a in announcements if a['id'] != announcement_id]
    _save_announcements(announcements)


def get_announcement_by_id(announcement_id):
    announcements = _load_announcements()
    for a in announcements:
        if a['id'] == announcement_id:
            return a
    return None
