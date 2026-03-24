from datetime import datetime, timedelta
from app.data import load_data, save_data
from app.courses.definition_service import (
    add_definition, list_definitions, get_definition_by_id,
    update_definition, delete_definition
)
from app.courses.session_service import (
    add_session, list_sessions, get_session_by_id,
    update_session, delete_session, cancel_session, get_sessions_for_week,
    get_sessions_by_teacher
)
from app.teachers.service import get_teacher_by_id
from app.classes.service import get_class_by_id
from app.rooms.service import get_room_by_id



def add_course(title, teacher_id, class_id, start_datetime, duration, mode, room_id=None):
    """Crée une définition de cours ET une séance en une seule opération."""
    definition = add_definition(title, teacher_id, class_id)
    session = add_session(definition['id'], start_datetime, duration, mode, room_id)
    return session  

def update_course(course_id, title=None, teacher_id=None, class_id=None,
                  start_datetime=None, duration=None, mode=None, room_id=None, is_canceled=None):

    if any(v is not None for v in [title, teacher_id, class_id]):
        update_definition(course_id, title, teacher_id, class_id)
    return get_definition_by_id(course_id)

def list_courses():
    """Retourne la liste des définitions de cours (sans données temporelles)."""
    definitions = list_definitions()
    enriched = []
    for d in definitions:
        teacher = get_teacher_by_id(d['teacher_id'])
        teacher_name = teacher['name'] if teacher else 'Inconnu'
        class_obj = get_class_by_id(d['class_id'])
        class_name = class_obj['name'] if class_obj else 'Non définie'
        enriched.append({
            'id': d['id'],
            'title': d['title'],
            'teacher_id': d['teacher_id'],
            'teacher_name': teacher_name,
            'class_id': d['class_id'],
            'class_name': class_name,
            'description': d.get('description', '')
        })
    return enriched

def get_course_by_id(course_id):
    """Retourne la définition du cours."""
    return get_definition_by_id(course_id)

def delete_course(course_id):
    """Supprime la définition du cours et ses séances associées."""
    sessions = list_sessions()
    for s in sessions:
        if s['course_id'] == course_id:
            delete_session(s['id'])
    delete_definition(course_id)

def search_courses(title):
    definitions = list_definitions()
    if not title:
        return definitions
    title = title.lower()
    return [d for d in definitions if title in d['title'].lower()]

def get_courses_for_week(start_date):
    """Renvoie les séances de la semaine (pour l'affichage du planning)."""
    return get_sessions_for_week(start_date)

def get_courses_by_teacher(teacher_id):
    definitions = list_definitions()
    return [d for d in definitions if d['teacher_id'] == teacher_id]