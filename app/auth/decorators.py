from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                flash('Accès non autorisé.', 'danger')
                return redirect(url_for('auth.login'))
            # Créer une nouvelle variable pour la liste, sans modifier allowed_roles
            roles = allowed_roles if isinstance(allowed_roles, list) else [allowed_roles]
            if session['user_role'] not in roles:
                flash('Vous n\'avez pas les droits pour accéder à cette page.', 'danger')
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator