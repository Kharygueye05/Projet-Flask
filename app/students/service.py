from app.data import load_data, save_data
from app.auth.service import create_user, get_user_by_email

STUDENTS_FILE = 'students.json'


def _load_students():
    return load_data(STUDENTS_FILE)


def _save_students(students):
    save_data(STUDENTS_FILE, students)


def _gen_matricule(students):
    num = str(len(students) + 1).zfill(4)
    return f"ETU-{num}"


def _gen_email(name, students):
    """Génère un email unique : prenom.nom@etu.univ.sn"""
    parts = name.strip().lower().split()
    base = f"{parts[0]}.{parts[-1]}" if len(parts) >= 2 else parts[0]
    email = f"{base}@etu.univ.sn"
    
    # Si l'email existe déjà, ajoute un numéro
    existing = [s['email'] for s in students]
    counter = 1
    while email in existing:
        email = f"{base}{counter}@etu.univ.sn"
        counter += 1
    
    return email



def add_student(name, sexe, date_naissance):
    students = _load_students()
    email = _gen_email(name, students)
    new_id    = max([s['id'] for s in students], default=0) + 1
    matricule = _gen_matricule(students)
    student = {
        'id'             : new_id,
        'matricule'      : matricule,
        'name'           : name.strip(),
        'email'          : email,
        'sexe'           : sexe,
        'date_naissance' : date_naissance,
        'class_id'       : None
    }
    students.append(student)
    _save_students(students)
    if not get_user_by_email(email):
        default_password = name.lower().replace(' ', '') + '123'
        create_user(email, default_password, name, role='student')
    return student

def list_students():
    return _load_students()

def get_student_by_email(email):
    students = _load_students()
    for s in students:
        if s['email'].lower() == email.lower():
            return s
    return None
def get_student_by_id(student_id):
    students = _load_students()
    for s in students:
        if s['id'] == student_id:
            return s
    return None


def update_student(student_id, name=None, email=None, sexe=None, date_naissance=None):
    students = _load_students()
    for s in students:
        if s['id'] == student_id:
            if name:
                s['name'] = name.strip()
            if email:
                s['email'] = email.strip()
            if sexe:
                s['sexe'] = sexe
            if date_naissance:
                s['date_naissance'] = date_naissance
            _save_students(students)
            return s
    return None


def delete_student(student_id):
    students = _load_students()
    students = [s for s in students if s['id'] != student_id]
    _save_students(students)


def search_students(query):
    students = _load_students()
    query = query.lower()
    return [
        s for s in students
        if query in s['name'].lower()
        or query in s['email'].lower()
        or query in s.get('matricule', '').lower()
    ]