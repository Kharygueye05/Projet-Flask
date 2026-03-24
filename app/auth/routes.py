from flask import render_template, request, flash, redirect, url_for, session
from app.auth import auth_bp
from app.auth.service import check_user, create_user, get_user_by_id, update_user, get_user_by_email
from app.auth.decorators import login_required


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = check_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            flash(f'Bienvenue {user["name"]} !', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if not name or not email or not password:
            flash('Tous les champs sont obligatoires.', 'danger')
        elif password != confirm:
            flash('Les mots de passe ne correspondent pas.', 'danger')
        elif get_user_by_email(email):
            flash('Cet email est déjà utilisé.', 'danger')
        else:
            create_user(email, password, name)
            flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_user_by_id(session['user_id'])
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new = request.form.get('confirm_new_password')

        # Vérification du mot de passe actuel
        if not check_user(user['email'], current_password):
            flash('Mot de passe actuel incorrect.', 'danger')
        else:
            # Mise à jour des informations
            update_data = {}
            if name and name != user['name']:
                update_data['name'] = name
            if email and email != user['email']:
                if get_user_by_email(email):
                    flash('Cet email est déjà utilisé par un autre compte.', 'danger')
                else:
                    update_data['email'] = email
            if new_password:
                if new_password != confirm_new:
                    flash('Les nouveaux mots de passe ne correspondent pas.', 'danger')
                else:
                    update_data['password'] = new_password

            if update_data:
                update_user(user['id'], **update_data)
                # Mettre à jour la session
                if 'name' in update_data:
                    session['user_name'] = update_data['name']
                if 'email' in update_data:
                    session['user_email'] = update_data['email']
                flash('Profil mis à jour avec succès.', 'success')
            else:
                flash('Aucune modification effectuée.', 'info')
            return redirect(url_for('auth.profile'))
    return render_template('auth/profile.html', user=user)