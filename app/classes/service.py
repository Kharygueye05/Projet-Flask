from app.data import load_data, save_data
from app.students.service import _load_students, _save_students

CLASSES_FILE = 'classes.json'

def _load_classes():
    return load_data(CLASSES_FILE)

def _save_classes(classes):
    save_data(CLASSES_FILE, classes)

def add_class(name, description=''):
    classes = _load_classes()
    new_id = max([c['id'] for c in classes], default=0) + 1
    cls = {'id': new_id, 'name': name, 'description': description, 'student_ids': []}
    classes.append(cls)
    _save_classes(classes)
    return cls

def list_classes():
    return _load_classes()

def get_class_by_id(class_id):
    classes = _load_classes()
    for c in classes:
        if c['id'] == class_id:
            return c
    return None

def update_class(class_id, name=None, description=None):
    classes = _load_classes()
    for c in classes:
        if c['id'] == class_id:
            if name:
                c['name'] = name
            if description:
                c['description'] = description
            _save_classes(classes)
            return c
    return None

def delete_class(class_id):
    classes = _load_classes()
    classes = [c for c in classes if c['id'] != class_id]
    _save_classes(classes)
    students = _load_students()
    for s in students:
        if s.get('class_id') == class_id:
            s['class_id'] = None
    _save_students(students)

def add_student_to_class(student_id, class_id):
    classes = _load_classes()
    for c in classes:
        if c['id'] == class_id and student_id not in c['student_ids']:
            c['student_ids'].append(student_id)
            _save_classes(classes)
            students = _load_students()
            for s in students:
                if s['id'] == student_id:
                    s['class_id'] = class_id
                    break
            _save_students(students)
            return True
    return False

def remove_student_from_class(student_id, class_id):
    classes = _load_classes()
    for c in classes:
        if c['id'] == class_id and student_id in c['student_ids']:
            c['student_ids'].remove(student_id)
            _save_classes(classes)
            students = _load_students()
            for s in students:
                if s['id'] == student_id:
                    s['class_id'] = None
                    break
            _save_students(students)
            return True
    return False

def get_students_in_class(class_id):
    students = _load_students()
    return [s for s in students if s.get('class_id') == class_id]