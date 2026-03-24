from flask import render_template, session
from app.dashboard import dashboard_bp
from app.students.service import list_students
from app.teachers.service import list_teachers
from app.courses.service import list_courses, get_sessions_by_teacher, list_sessions
from app.classes.service import list_classes
from app.auth.decorators import login_required

def get_teacher_by_email(email):
    from app.teachers.service import _load_teachers
    teachers = _load_teachers()
    for t in teachers:
        if t['email'] == email:
            return t
    return None

def get_student_by_email(email):
    from app.students.service import _load_students
    students = _load_students()
    for s in students:
        if s['email'] == email:
            return s
    return None

@dashboard_bp.route('/')
@login_required
def index():
    role = session.get('user_role')
    if role == 'admin':
        students = list_students()
        teachers = list_teachers()
        classes = list_classes()
        courses = list_courses()
        total_students = len(students)
        total_teachers = len(teachers)
        total_classes = len(classes)
        total_courses = len(courses)
        # Statistiques par classe
        class_stats = []
        for cls in classes:
            class_students = [s for s in students if s.get('class_id') == cls['id']]
            class_courses = [c for c in courses if c['class_id'] == cls['id']]
            class_stats.append({
                'name': cls['name'],
                'students_count': len(class_students),
                'courses_count': len(class_courses)
            })
        # Derniers étudiants
        latest_students = sorted(students, key=lambda s: s['id'], reverse=True)[:5]
        # Derniers cours
        raw_courses = list_courses()
        latest_courses = sorted(raw_courses, key=lambda c: c['id'], reverse=True)[:5]
        latest_courses_info = []
        teachers_list = list_teachers()
        classes_list = list_classes()
        for rc in latest_courses:
            teacher = next((t for t in teachers_list if t['id'] == rc['teacher_id']), None)
            cls = next((c for c in classes_list if c['id'] == rc['class_id']), None)
            latest_courses_info.append({
                'title': rc['title'],
                'teacher_name': teacher['name'] if teacher else 'Inconnu',
                'class_name': cls['name'] if cls else 'Inconnue'
            })
        return render_template('dashboard/admin.html',
                               total_students=total_students,
                               total_teachers=total_teachers,
                               total_classes=total_classes,
                               total_courses=total_courses,
                               class_stats=class_stats,
                               latest_students=latest_students,
                               latest_courses=latest_courses_info)
    elif role == 'teacher':
        teacher = get_teacher_by_email(session['user_email'])
        if teacher:
            all_courses = list_courses()
            my_courses = [c for c in all_courses if c['teacher_id'] == teacher['id']]
            # Compter les étudiants dans ses cours (unique)
            student_ids = set()
            for c in my_courses:
                # Récupérer les étudiants de la classe
                from app.classes.service import get_students_in_class
                if c['class_id']:
                    students_in_class = get_students_in_class(c['class_id'])
                    student_ids.update(s['id'] for s in students_in_class)
            total_students_taught = len(student_ids)
            my_sessions = get_sessions_by_teacher(teacher['id'])
            return render_template('dashboard/teacher.html', teacher=teacher, courses=my_courses, total_students_taught=total_students_taught, sessions=my_sessions)
        else:
            return render_template('dashboard/teacher.html', teacher=None, courses=[], sessions=[])
    else:  # student
        student = get_student_by_email(session['user_email'])
        if student and student.get('class_id'):
            from app.classes.service import get_class_by_id
            cls = get_class_by_id(student['class_id'])
            class_name = cls['name'] if cls else 'Non définie'
            all_courses = list_courses()
            my_courses = [c for c in all_courses if c['class_id'] == student['class_id']]
            my_sessions = [s for s in list_sessions() if s['class_id'] == student['class_id']]
            return render_template('dashboard/student.html', student=student, class_name=class_name, courses=my_courses, sessions=my_sessions)
        else:
            return render_template('dashboard/student.html', student=student, class_name='Aucune', courses=[], sessions=[])
        if student and student.get('class_id'):
            from app.classes.service import get_class_by_id
            cls = get_class_by_id(student['class_id'])
            class_name = cls['name'] if cls else 'Non définie'
            all_courses = list_courses()
            my_courses = [c for c in all_courses if c['class_id'] == student['class_id']]
            return render_template('dashboard/student.html', student=student, class_name=class_name, courses=my_courses)
        else:
            return render_template('dashboard/student.html', student=student, class_name='Aucune', courses=[])