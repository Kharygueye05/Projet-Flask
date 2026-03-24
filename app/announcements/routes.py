from flask import render_template, request, flash, redirect, url_for, session
from app.announcements import announcements_bp
from app.announcements.service import (
    list_announcements, add_announcement, delete_announcement, get_announcement_by_id
)
from app.auth.decorators import login_required, role_required

@announcements_bp.route('/')
@login_required
def list_announcements_view():
    announcements = list_announcements()
    return render_template('announcements/list.html', announcements=announcements)

@announcements_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_announcement():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = session.get('user_name', 'Admin')
        if not title or not content:
            flash('Titre et contenu requis.', 'danger')
        else:
            add_announcement(title, content, author)
            flash('Annonce publiée.', 'success')
            return redirect(url_for('announcements.list_announcements_view'))
    return render_template('announcements/create.html')

@announcements_bp.route('/delete/<int:id>')
@login_required
@role_required('admin')
def delete_announcement_view(id):
    announcement = get_announcement_by_id(id)
    if announcement:
        delete_announcement(id)
        flash('Annonce supprimée.', 'info')
    else:
        flash('Annonce introuvable.', 'danger')
    return redirect(url_for('announcements.list_announcements_view'))
