from flask import render_template, request, flash, redirect, url_for
from app.students import students_bp
from app.students.service import (
    add_student, list_students, delete_student, get_student_by_id,
    update_student, search_students, _gen_matricule, _load_students, get_student_by_email
)
from app.auth.decorators import login_required, role_required


@students_bp.route('/')
@login_required
@role_required('admin')
def list():
    page             = request.args.get('page', 1, type=int)
    search_matricule = request.args.get('search_matricule', '').strip()
    search_email     = request.args.get('search_email', '').strip()
    per_page         = 5

    all_students = list_students()

    # Filtrage
    if search_matricule:
        all_students = [s for s in all_students if search_matricule.lower() in s['matricule'].lower()]
    if search_email:
        all_students = [s for s in all_students if search_email.lower() in s['email'].lower()]

    total       = len(all_students)
    total_pages = max(1, (total + per_page - 1) // per_page)
    start       = (page - 1) * per_page
    paginated   = all_students[start:start + per_page]

    return render_template(
        'students/list.html',
        students=paginated,
        page=page,
        total_pages=total_pages,
        search_matricule=search_matricule,
        search_email=search_email
    )


@students_bp.route('/search')
@login_required
@role_required('admin')
def search():
    query = request.args.get('q', '')
    results = search_students(query) if query else []
    return render_template('students/search.html', query=query, results=results)


@students_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create():
    if request.method == 'POST':
        name           = request.form.get('name', '').strip()
        sexe           = request.form.get('sexe', '').strip()
        date_naissance = request.form.get('date_naissance', '').strip()

        if name and sexe and date_naissance:
            student = add_student(name, sexe, date_naissance)
            if student:
                flash(f'Étudiant ajouté. Email : {student["email"]} — Mot de passe : {name.lower().replace(" ", "")}123', 'success')
                return redirect(url_for('students.list'))
        else:
            flash('Tous les champs sont requis.', 'danger')

    matricule = _gen_matricule(_load_students())
    return render_template('students/create.html', matricule=matricule)


@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    student = get_student_by_id(id)
    if not student:
        flash('Étudiant introuvable.', 'danger')
        return redirect(url_for('students.list'))

    if request.method == 'POST':
        name           = request.form.get('name', '').strip()
        email          = request.form.get('email', '').strip()
        sexe           = request.form.get('sexe', '').strip()
        date_naissance = request.form.get('date_naissance', '').strip()

        if name and sexe and date_naissance:
            update_student(id, name=name, email=email, sexe=sexe, date_naissance=date_naissance)

            from app.auth.service import get_user_by_email, update_user
            user = get_user_by_email(student['email'])
            if user:
                update_user(user['id'], name=name, email=email)

            flash('Étudiant modifié avec succès.', 'success')
            return redirect(url_for('students.list'))
        else:
            flash('Tous les champs obligatoires doivent être remplis.', 'danger')

    return render_template('students/edit.html', student=student)


@students_bp.route('/delete/<int:id>')
@login_required
@role_required('admin')
def delete(id):
    delete_student(id)
    flash('Étudiant supprimé avec succès.', 'info')
    return redirect(url_for('students.list'))