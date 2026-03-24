from app.data import load_data, save_data
from app.auth.service import create_user, get_user_by_email

TEACHERS_FILE = 'teachers.json'

def _load_teachers():
    return load_data(TEACHERS_FILE)

def _save_teachers(teachers):
    save_data(TEACHERS_FILE, teachers)

def add_teacher(name, email, specialities):
    # specialities est une liste
    teachers = _load_teachers()
    new_id = max([t['id'] for t in teachers], default=0) + 1
    teacher = {
        'id': new_id,
        'name': name,
        'email': email,
        'specialities': specialities
    }
    teachers.append(teacher)
    _save_teachers(teachers)
    # Création automatique du compte utilisateur
    if not get_user_by_email(email):
        default_password = name.lower().replace(' ', '') + '123'
        create_user(email, default_password, name, role='teacher')
    return teacher

def list_teachers():
    return _load_teachers()

def get_teacher_by_id(teacher_id):
    teachers = _load_teachers()
    for t in teachers:
        if t['id'] == teacher_id:
            return t
    return None


def get_teacher_by_email(email):
    teachers = _load_teachers()
    for t in teachers:
        if t['email'].lower() == email.lower():
            return t
    return None


def update_teacher(teacher_id, name=None, email=None, specialities=None):
    teachers = _load_teachers()
    for t in teachers:
        if t['id'] == teacher_id:
            if name:
                t['name'] = name
            if email:
                t['email'] = email
            if specialities is not None:
                t['specialities'] = specialities
            _save_teachers(teachers)
            return t
    return None

def delete_teacher(teacher_id):
    teachers = _load_teachers()
    teachers = [t for t in teachers if t['id'] != teacher_id]
    _save_teachers(teachers)

def search_teachers(query):
    teachers = _load_teachers()
    query = query.lower()
    return [t for t in teachers if query in t['name'].lower() or query in t['email'].lower() or any(query in spec.lower() for spec in t['specialities'])]

def filter_by_speciality(speciality):
    teachers = _load_teachers()
    if not speciality:
        return teachers
    return [t for t in teachers if speciality.lower() in [s.lower() for s in t['specialities']]]