from flask import Blueprint

teachers_bp = Blueprint('teachers', __name__, template_folder='templates')

from app.teachers import routes