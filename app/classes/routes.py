from flask import render_template, request, flash, redirect, url_for
from app.classes import classes_bp
from app.classes.service import (
    add_class, list_classes, delete_class, get_class_by_id,
    update_class, add_student_to_class, remove_student_from_class,
    get_students_in_class
)
from app.students.service import list_students
from app.auth.decorators import login_required, role_required

@classes_bp.route('/')
@login_required
@role_required('admin')
def list():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    all_classes = list_classes()
    total = len(all_classes)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_classes[start:end]
    return render_template('classes/list.html', classes=paginated,
                           page=page, total_pages=total_pages)

@classes_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            add_class(name, description)
            flash('Classe créée.', 'success')
            return redirect(url_for('classes.list'))
        else:
            flash('Le nom de la classe est requis.', 'danger')
    return render_template('classes/create.html')

@classes_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    cls = get_class_by_id(id)
    if not cls:
        flash('Classe introuvable.', 'danger')
        return redirect(url_for('classes.list'))
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            update_class(id, name=name, description=description)
            flash('Classe modifiée.', 'success')
            return redirect(url_for('classes.list'))
        else:
            flash('Le nom de la classe est requis.', 'danger')
    return render_template('classes/edit.html', cls=cls)

@classes_bp.route('/delete/<int:id>')
@login_required
@role_required('admin')
def delete(id):
    delete_class(id)
    flash('Classe supprimée.', 'info')
    return redirect(url_for('classes.list'))

@classes_bp.route('/manage/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage(id):
    cls = get_class_by_id(id)
    if not cls:
        flash('Classe introuvable.', 'danger')
        return redirect(url_for('classes.list'))

    all_students = list_students()
    enrolled_students = get_students_in_class(id)
    enrolled_ids = [s['id'] for s in enrolled_students]

    available_students = [s for s in all_students if s.get('class_id') is None and s['id'] not in enrolled_ids]

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        action = request.form.get('action')
        if student_id and action == 'add':
            if add_student_to_class(int(student_id), id):
                flash('Étudiant ajouté à la classe.', 'success')
            else:
                flash('Erreur lors de l\'ajout.', 'danger')
        elif student_id and action == 'remove':
            if remove_student_from_class(int(student_id), id):
                flash('Étudiant retiré de la classe.', 'info')
            else:
                flash('Erreur lors du retrait.', 'danger')
        return redirect(url_for('classes.manage', id=id))

    return render_template('classes/manage.html', cls=cls,
                           enrolled_students=enrolled_students,
                           available_students=available_students)