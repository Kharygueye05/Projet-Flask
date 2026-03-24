from flask import render_template, request, flash, redirect, url_for, session
from app.teachers import teachers_bp
from app.teachers.service import (
    add_teacher, list_teachers, delete_teacher, get_teacher_by_id,
    get_teacher_by_email, update_teacher, search_teachers, filter_by_speciality
)
from app.students.service import list_students
from app.auth.decorators import login_required, role_required
from app.auth.service import create_user, get_user_by_email

@teachers_bp.route('/')
@login_required
@role_required('admin')   # seul l'admin voit la liste
def list():
    speciality = request.args.get('speciality', '')
    if speciality:
        teachers = filter_by_speciality(speciality)
    else:
        teachers = list_teachers()
    all_specialities = sorted(set(spec for t in list_teachers() for spec in t['specialities']))
    return render_template('teachers/list.html', teachers=teachers, speciality=speciality, all_specialities=all_specialities)

@teachers_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        specialities = request.form.getlist('specialities')  # champ multi-sélection
        if not specialities:
            specialities = request.form.get('speciality', '').split(',')  # fallback
        specialities = [s.strip() for s in specialities if s.strip()]
        if name and email and specialities:
            # Vérifier si un utilisateur existe déjà avec cet email
            if get_user_by_email(email):
                flash('Un compte existe déjà avec cet email.', 'danger')
            else:
                # Créer le compte enseignant avec un mot de passe par défaut (nom + 123)
                default_password = name.lower().replace(' ', '') + '123'
                create_user(email, default_password, name, role='teacher')
                add_teacher(name, email, specialities)
                flash(f'Enseignant ajouté. Son mot de passe est : {default_password}', 'success')
                return redirect(url_for('teachers.list'))
        else:
            flash('Tous les champs sont requis.', 'danger')
    return render_template('teachers/create.html')

@teachers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    teacher = get_teacher_by_id(id)
    if not teacher:
        flash('Enseignant introuvable.', 'danger')
        return redirect(url_for('teachers.list'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        specialities = request.form.getlist('specialities')
        if not specialities:
            specialities = request.form.get('speciality', '').split(',')
        specialities = [s.strip() for s in specialities if s.strip()]
        if name and email and specialities:
            update_teacher(id, name=name, email=email, specialities=specialities)
            # Mettre à jour aussi le compte utilisateur correspondant
            user = get_user_by_email(teacher['email'])
            if user:
                from app.auth.service import update_user
                update_user(user['id'], name=name, email=email)
            flash('Enseignant modifié.', 'success')
            return redirect(url_for('teachers.list'))
        else:
            flash('Tous les champs sont requis.', 'danger')
    return render_template('teachers/edit.html', teacher=teacher)

@teachers_bp.route('/delete/<int:id>')
@login_required
@role_required('admin')
def delete(id):
    teacher = get_teacher_by_id(id)
    if teacher:
        delete_teacher(id)
        # Optionnel : supprimer aussi le compte utilisateur
        user = get_user_by_email(teacher['email'])
        if user:
            from app.auth.service import _load_users, _save_users
            users = _load_users()
            users = [u for u in users if u['id'] != user['id']]
            _save_users(users)
        flash('Enseignant supprimé.', 'info')
    else:
        flash('Enseignant introuvable.', 'danger')
    return redirect(url_for('teachers.list'))

@teachers_bp.route('/search')
@login_required
@role_required('admin')
def search():
    query = request.args.get('q', '')
    if query:
        results = search_teachers(query)
    else:
        results = []
    return render_template('teachers/search.html', query=query, results=results)


@teachers_bp.route('/<int:id>')
@login_required
def detail(id):
    teacher = get_teacher_by_id(id)
    if not teacher:
        flash('Enseignant introuvable.', 'danger')
        return redirect(url_for('teachers.list'))

    if session.get('user_role') == 'teacher' and session.get('user_email') != teacher['email']:
        flash('Accès refusé à ce profil.', 'danger')
        return redirect(url_for('dashboard.index'))

    from app.courses.service import get_courses_by_teacher
    courses = get_courses_by_teacher(id)
    class_ids = sorted({c['class_id'] for c in courses if c.get('class_id')})
    students = list_students()
    student_count = len({s['id'] for s in students if s.get('class_id') in class_ids})

    return render_template('teachers/detail.html', teacher=teacher, courses=courses,
                           student_count=student_count, class_count=len(class_ids))


@teachers_bp.route('/me')
@login_required
def my_profile():
    if session.get('user_role') != 'teacher':
        flash('Accès réservé aux enseignants.', 'danger')
        return redirect(url_for('dashboard.index'))

    teacher = get_teacher_by_email(session.get('user_email'))
    if teacher:
        return redirect(url_for('teachers.detail', id=teacher['id']))

    flash('Profil enseignant introuvable.', 'danger')
    return redirect(url_for('dashboard.index'))
