from app.data import load_data, save_data

USERS_FILE = 'users.json'

def _load_users():
    return load_data(USERS_FILE)

def _save_users(users):
    save_data(USERS_FILE, users)

def get_user_by_email(email):
    users = _load_users()
    for user in users:
        if user['email'] == email:
            return user
    return None

def check_user(email, password):
    user = get_user_by_email(email)
    if user and user['password'] == password:
        return user
    return None

def create_user(email, password, name, role='student'):
    """Crée un nouvel utilisateur (admin, teacher, student)."""
    users = _load_users()
    new_id = max([u['id'] for u in users], default=0) + 1
    user = {
        'id': new_id,
        'email': email,
        'password': password,
        'name': name,
        'role': role
    }
    users.append(user)
    _save_users(users)
    return user

def get_user_by_id(user_id):
    users = _load_users()
    for u in users:
        if u['id'] == user_id:
            return u
    return None

def update_user(user_id, **kwargs):
    users = _load_users()
    for user in users:
        if user['id'] == user_id:
            user.update(kwargs)
            _save_users(users)
            return user
    return None