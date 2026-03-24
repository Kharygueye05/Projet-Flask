from flask import render_template, request, flash, redirect, url_for, session
from datetime import datetime, timedelta
from app.courses import courses_bp
from app.courses.service import (
    add_course, list_courses, delete_course, get_course_by_id,
    update_course, search_courses, get_courses_for_week
)
from app.courses.session_service import (
    add_session, list_sessions, get_session_by_id, update_session,
    delete_session, cancel_session, get_sessions_for_week
)
from app.courses.definition_service import list_definitions, get_definition_by_id
from app.teachers.service import list_teachers
from app.classes.service import list_classes
from app.rooms.service import list_rooms
from app.auth.decorators import login_required, role_required
from app.students.service import get_student_by_email

def get_teacher_by_email(email):
    from app.teachers.service import _load_teachers
    teachers = _load_teachers()
    for t in teachers:
        if t['email'] == email:
            return t
    return None


@courses_bp.route('/')
@login_required
def list():
    role = session.get('user_role')
    q = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    all_courses = list_courses()
    if q:
        all_courses = search_courses(q)

    if role == 'admin':
        filtered = all_courses
    elif role == 'teacher':
        teacher = get_teacher_by_email(session['user_email'])
        if teacher:
            filtered = [c for c in all_courses if c['teacher_id'] == teacher['id']]
        else:
            flash('Enseignant non trouvé.', 'danger')
            return redirect(url_for('dashboard.index'))
    else:  # student
        student = get_student_by_email(session['user_email'])
        if student and student.get('class_id'):
            filtered = [c for c in all_courses if c['class_id'] == student['class_id']]
        else:
            filtered = []
            flash('Aucune classe affectée.', 'info')

    total = len(filtered)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]


    if role == 'admin':
        template = 'courses/list.html'
    elif role == 'teacher':
        template = 'courses/teacher_courses.html'
    else:
        template = 'courses/student_courses.html'

    return render_template(template, courses=paginated, query=q,
                           page=page, total_pages=total_pages)

@courses_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create():
    teachers = list_teachers()
    classes = list_classes()
    if request.method == 'POST':
        title = request.form.get('title')
        teacher_id = request.form.get('teacher_id')
        class_id = request.form.get('class_id')
        description = request.form.get('description', '')

        if not all([title, teacher_id, class_id]):
            flash('Titre, enseignant et classe sont requis.', 'danger')
            return redirect(url_for('courses.create'))

        try:
            teacher_id = int(teacher_id)
            class_id = int(class_id)
        except ValueError:
            flash('Données invalides.', 'danger')
            return redirect(url_for('courses.create'))

        from app.courses.definition_service import add_definition
        add_definition(title, teacher_id, class_id, description)
        flash('Cours créé avec succès.', 'success')
        return redirect(url_for('courses.list'))

    return render_template('courses/create.html', teachers=teachers, classes=classes)

@courses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    course = get_course_by_id(id)
    if not course:
        flash('Cours introuvable.', 'danger')
        return redirect(url_for('courses.list'))
    teachers = list_teachers()
    classes = list_classes()

    if request.method == 'POST':
        title = request.form.get('title')
        teacher_id = request.form.get('teacher_id')
        class_id = request.form.get('class_id')
        description = request.form.get('description', '')

        if not all([title, teacher_id, class_id]):
            flash('Titre, enseignant et classe sont requis.', 'danger')
            return redirect(url_for('courses.edit', id=id))

        try:
            teacher_id = int(teacher_id)
            class_id = int(class_id)
        except ValueError:
            flash('Données invalides.', 'danger')
            return redirect(url_for('courses.edit', id=id))

        from app.courses.definition_service import update_definition
        update_definition(id, title=title, teacher_id=teacher_id, class_id=class_id, description=description)
        flash('Cours modifié.', 'success')
        return redirect(url_for('courses.list'))

    return render_template('courses/edit.html', course=course, teachers=teachers, classes=classes)

@courses_bp.route('/delete/<int:id>')
@login_required
@role_required('admin')
def delete(id):
    delete_course(id)
    flash('Cours supprimé.', 'info')
    return redirect(url_for('courses.list'))


@courses_bp.route('/sessions')
@login_required
def sessions_list():
    role = session.get('user_role')
    course_id_filter = request.args.get('course_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 8

    all_sessions = list_sessions()
    if role == 'admin':
        filtered = all_sessions
    elif role == 'teacher':
        teacher = get_teacher_by_email(session['user_email'])
        if teacher:
            filtered = [s for s in all_sessions if s['teacher_id'] == teacher['id']]
        else:
            flash('Enseignant non trouvé.', 'danger')
            return redirect(url_for('dashboard.index'))
    else:  # student
        student = get_student_by_email(session['user_email'])
        if student and student.get('class_id'):
            filtered = [s for s in all_sessions if s['class_id'] == student['class_id']]
        else:
            filtered = []
            flash('Aucune classe affectée.', 'info')

    if course_id_filter:
        filtered = [s for s in filtered if s['course_id'] == course_id_filter]

    total = len(filtered)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]

    return render_template('courses/sessions_list.html', sessions=paginated,
                           page=page, total_pages=total_pages)

@courses_bp.route('/sessions/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_session():
    courses = list_courses()  
    rooms = list_rooms()
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        duration = request.form.get('duration')
        mode = request.form.get('mode')
        room_id = request.form.get('room_id') if mode == 'Présentiel' else None

        if not all([course_id, date_str, time_str, duration, mode]):
            flash('Tous les champs sont requis.', 'danger')
            return redirect(url_for('courses.create_session'))

        if mode == 'Présentiel' and not room_id:
            flash('Une salle doit être sélectionnée pour un cours en présentiel.', 'danger')
            return redirect(url_for('courses.create_session'))

        try:
            start_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            duration = int(duration)
            course_id = int(course_id)
            if room_id:
                room_id = int(room_id)
        except ValueError:
            flash('Données invalides.', 'danger')
            return redirect(url_for('courses.create_session'))

        try:
            add_session(course_id, start_datetime, duration, mode, room_id)
            flash('Séance créée.', 'success')
            return redirect(url_for('courses.sessions_list'))
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('courses.create_session'))

    return render_template('courses/session_create.html', courses=courses, rooms=rooms)

@courses_bp.route('/sessions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_session(id):
    session = get_session_by_id(id)
    if not session:
        flash('Séance introuvable.', 'danger')
        return redirect(url_for('courses.sessions_list'))
    rooms = list_rooms()
    if request.method == 'POST':
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        duration = request.form.get('duration')
        mode = request.form.get('mode')
        room_id = request.form.get('room_id') if mode == 'Présentiel' else None

        if not all([date_str, time_str, duration, mode]):
            flash('Tous les champs sont requis.', 'danger')
            return redirect(url_for('courses.edit_session', id=id))

        try:
            start_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            duration = int(duration)
            if room_id:
                room_id = int(room_id)
        except ValueError:
            flash('Données invalides.', 'danger')
            return redirect(url_for('courses.edit_session', id=id))

        try:
            update_session(id, start_datetime=start_datetime, duration=duration, mode=mode, room_id=room_id)
            flash('Séance modifiée.', 'success')
            return redirect(url_for('courses.sessions_list'))
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('courses.edit_session', id=id))

    start_dt = datetime.fromisoformat(session['start_datetime'])
    session_date = start_dt.strftime("%Y-%m-%d")
    session_time = start_dt.strftime("%H:%M")
    return render_template('courses/session_edit.html', session=session, rooms=rooms,
                           session_date=session_date, session_time=session_time)

@courses_bp.route('/sessions/delete/<int:id>')
@login_required
@role_required('admin')
def delete_session_route(id):
    delete_session(id)
    flash('Séance supprimée.', 'info')
    return redirect(url_for('courses.sessions_list'))

@courses_bp.route('/sessions/cancel/<int:id>')
@login_required
def cancel_session_route(id):
    role = session.get('user_role')
    course_session = get_session_by_id(id)
    if not course_session:
        flash('Séance introuvable.', 'danger')
        return redirect(url_for('courses.sessions_list'))
    if role == 'admin':
        cancel_session(id)
        flash('Séance annulée.', 'warning')
    elif role == 'teacher':
        teacher = get_teacher_by_email(session['user_email'])
        if teacher and course_session['teacher_id'] == teacher['id']:
            cancel_session(id)
            flash('Séance annulée.', 'warning')
        else:
            flash('Vous ne pouvez pas annuler cette séance.', 'danger')
    else:
        flash('Vous n\'avez pas le droit d\'annuler une séance.', 'danger')
    return redirect(url_for('courses.sessions_list'))



@courses_bp.route('/schedule/week')
@login_required
def week_schedule():
    role = session.get('user_role')
    date_param = request.args.get('date')
    if date_param:
        try:
            base_date = datetime.strptime(date_param, "%Y-%m-%d")
        except ValueError:
            base_date = datetime.now()
    else:
        base_date = datetime.now()
    start_of_week = base_date - timedelta(days=base_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    all_sessions = get_sessions_for_week(start_of_week)

    if role == 'admin':
        sessions = all_sessions
        page_title = 'Planning du'
    elif role == 'teacher':
        teacher = get_teacher_by_email(session['user_email'])
        if teacher:
            sessions = [s for s in all_sessions if s['teacher_id'] == teacher['id']]
            page_title = 'Mon emploi du temps'
        else:
            flash('Enseignant non trouvé.', 'danger')
            return redirect(url_for('dashboard.index'))
    else:  # student
        student = get_student_by_email(session['user_email'])
        if student and student.get('class_id'):
            sessions = [s for s in all_sessions if s['class_id'] == student['class_id']]
            page_title = 'Mon emploi du temps'
        else:
            sessions = []
            page_title = 'Mon emploi du temps'
            flash('Aucune classe affectée.', 'info')

    week_days = []
    for i in range(7):
        day_date = start_of_week + timedelta(days=i)
        day_sessions = [s for s in sessions if s['start_datetime'].date() == day_date.date()]
        week_days.append({'date': day_date, 'courses': day_sessions})

    return render_template('courses/week_schedule.html', week_days=week_days,
                           start_of_week=start_of_week,
                           prev_week=start_of_week - timedelta(days=7),
                           next_week=start_of_week + timedelta(days=7),
                           page_title=page_title,
                           timedelta=timedelta)

@courses_bp.route('/schedule')
@login_required
def schedule():
    return redirect(url_for('courses.week_schedule'))

@courses_bp.route('/my_schedule')
@login_required
def my_schedule():
    if session.get('user_role') != 'student':
        flash('Accès réservé aux étudiants.', 'danger')
        return redirect(url_for('courses.list'))
    student = get_student_by_email(session['user_email'])
    if not student:
        flash('Étudiant non trouvé.', 'danger')
        return redirect(url_for('dashboard.index'))
    all_sessions = list_sessions()
    if student.get('class_id'):
        sessions = [s for s in all_sessions if s['class_id'] == student['class_id']]
    else:
        sessions = []
        flash('Vous n\'êtes affecté à aucune classe.', 'info')
    return render_template('courses/my_schedule.html', courses=sessions)

@courses_bp.route('/teacher_schedule')
@login_required
def teacher_schedule():
    if session.get('user_role') != 'teacher':
        flash('Accès réservé aux enseignants.', 'danger')
        return redirect(url_for('courses.list'))
    teacher = get_teacher_by_email(session['user_email'])
    if not teacher:
        flash('Enseignant non trouvé.', 'danger')
        return redirect(url_for('dashboard.index'))
    all_sessions = list_sessions()
    sessions = [s for s in all_sessions if s['teacher_id'] == teacher['id']]
    return render_template('courses/teacher_schedule.html', courses=sessions)