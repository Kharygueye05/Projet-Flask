from flask import Blueprint

classes_bp = Blueprint('classes', __name__, template_folder='templates')

from app.classes import routes