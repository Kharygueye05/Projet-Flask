from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'votre_cle_secrète_très_longue'

    # Enregistrement des blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.students import students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    from app.teachers import teachers_bp
    app.register_blueprint(teachers_bp, url_prefix='/teachers')

    from app.courses import courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    from app.classes import classes_bp
    app.register_blueprint(classes_bp, url_prefix='/classes')

    from app.announcements import announcements_bp
    app.register_blueprint(announcements_bp, url_prefix='/announcements')

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)  # pas de préfixe, route racine
    from app.rooms.service import init_rooms
    init_rooms()  

    return app