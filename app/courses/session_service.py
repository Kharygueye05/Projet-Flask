from datetime import datetime, timedelta
from app.data import load_data, save_data
from app.teachers.service import get_teacher_by_id
from app.classes.service import get_class_by_id
from app.rooms.service import get_room_by_id
from app.courses.definition_service import get_definition_by_id

SESSIONS_FILE = 'sessions.json'

def _load_sessions():
    return load_data(SESSIONS_FILE)

def _save_sessions(sessions):
    save_data(SESSIONS_FILE, sessions)

def _check_conflicts(start_dt, duration, teacher_id=None, class_id=None, room_id=None, exclude_session_id=None):
    sessions = _load_sessions()
    start = start_dt
    end = start_dt + timedelta(minutes=duration)

    for s in sessions:
        if exclude_session_id and s['id'] == exclude_session_id:
            continue
        s_start = datetime.fromisoformat(s['start_datetime'])
        s_end = s_start + timedelta(minutes=s['duration'])

        if start < s_end and end > s_start:
            if teacher_id and s['teacher_id'] == teacher_id:
                return True, f"Conflit avec la séance du cours '{s['title']}' pour ce professeur."
            if class_id and s['class_id'] == class_id:
                return True, f"Conflit avec la séance du cours '{s['title']}' pour cette classe."
            if room_id and s.get('room_id') == room_id:
                return True, f"Conflit avec la séance du cours '{s['title']}' pour cette salle."
    return False, ""

def add_session(course_id, start_datetime, duration, mode, room_id=None):
    definition = get_definition_by_id(course_id)
    if not definition:
        raise ValueError("Cours introuvable")

    teacher_id = definition['teacher_id']
    class_id = definition['class_id']

    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        raise ValueError("Enseignant introuvable")
    class_obj = get_class_by_id(class_id)
    if not class_obj:
        raise ValueError("Classe introuvable")

    if mode == "Présentiel":
        if not room_id:
            raise ValueError("Une salle est obligatoire en présentiel")
        room = get_room_by_id(room_id)
        if not room:
            raise ValueError("Salle introuvable")
    else:
        room_id = None

    conflict, msg = _check_conflicts(
        start_datetime, duration,
        teacher_id=teacher_id,
        class_id=class_id,
        room_id=room_id
    )
    if conflict:
        raise ValueError(msg)

    sessions = _load_sessions()
    new_id = max([s['id'] for s in sessions], default=0) + 1
    session = {
        'id': new_id,
        'course_id': course_id,
        'title': definition['title'],
        'teacher_id': teacher_id,
        'class_id': class_id,
        'start_datetime': start_datetime.isoformat(),
        'duration': duration,
        'mode': mode,
        'room_id': room_id,
        'is_canceled': False
    }
    sessions.append(session)
    _save_sessions(sessions)
    return session

def update_session(session_id, start_datetime=None, duration=None, mode=None, room_id=None, is_canceled=None):
    sessions = _load_sessions()
    session = None
    for s in sessions:
        if s['id'] == session_id:
            session = s
            break
    if not session:
        return None

    new_start = start_datetime if start_datetime is not None else datetime.fromisoformat(session['start_datetime'])
    new_duration = duration if duration is not None else session['duration']
    new_mode = mode if mode is not None else session['mode']
    new_room = room_id if room_id is not None else session.get('room_id')

    teacher_id = session['teacher_id']
    class_id = session['class_id']

    if new_mode == "Présentiel":
        if not new_room:
            raise ValueError("Une salle est obligatoire en présentiel")
        if room_id and not get_room_by_id(room_id):
            raise ValueError("Salle introuvable")
    else:
        new_room = None

    conflict, msg = _check_conflicts(
        new_start, new_duration,
        teacher_id=teacher_id,
        class_id=class_id,
        room_id=new_room,
        exclude_session_id=session_id
    )
    if conflict:
        raise ValueError(msg)

    if start_datetime is not None:
        session['start_datetime'] = start_datetime.isoformat()
    if duration is not None:
        session['duration'] = duration
    if mode is not None:
        session['mode'] = mode
    if room_id is not None or (mode is not None and mode == "Distanciel"):
        session['room_id'] = new_room
    if is_canceled is not None:
        session['is_canceled'] = is_canceled

    _save_sessions(sessions)
    return session

def list_sessions():
    sessions = _load_sessions()
    enriched = []
    french_days = {
        'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'
    }
    for s in sessions:
        teacher = get_teacher_by_id(s['teacher_id'])
        teacher_name = teacher['name'] if teacher else 'Inconnu'
        class_obj = get_class_by_id(s['class_id'])
        class_name = class_obj['name'] if class_obj else 'Non définie'
        room_name = None
        if s.get('room_id'):
            room = get_room_by_id(s['room_id'])
            room_name = room['name'] if room else None

        start_dt = datetime.fromisoformat(s['start_datetime'])
        day = start_dt.strftime('%A')
        day_fr = french_days.get(day, day)
        time_str = start_dt.strftime('%H:%M')
        room_display = room_name if room_name else ('En ligne' if s['mode'] == 'Distanciel' else 'Non définie')
        enriched.append({
            'id': s['id'],
            'course_id': s['course_id'],
            'title': s['title'],
            'teacher_name': teacher_name,
            'teacher_id': s['teacher_id'],
            'class_name': class_name,
            'class_id': s['class_id'],
            'start_datetime': start_dt,
            'duration': s['duration'],
            'mode': s['mode'],
            'room_name': room_name,
            'room_id': s.get('room_id'),
            'is_canceled': s.get('is_canceled', False),
            'schedule': {
                'day': day_fr,
                'time': time_str,
                'room': room_display,
                'mode': s['mode']
            }
        })
    return enriched

def get_session_by_id(session_id):
    sessions = _load_sessions()
    for s in sessions:
        if s['id'] == session_id:
            return s
    return None

def delete_session(session_id):
    sessions = _load_sessions()
    sessions = [s for s in sessions if s['id'] != session_id]
    _save_sessions(sessions)

def cancel_session(session_id):
    return update_session(session_id, is_canceled=True)

def get_sessions_for_week(start_date):
    end_date = start_date + timedelta(days=7)
    sessions = list_sessions()
    week_sessions = [s for s in sessions if start_date <= s['start_datetime'] < end_date]
    week_sessions.sort(key=lambda x: x['start_datetime'])
    return week_sessions

def get_sessions_by_teacher(teacher_id):
    return [s for s in list_sessions() if s['teacher_id'] == teacher_id]