from flask import Blueprint, render_template
from flask_security import login_required, current_user

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return render_template('index.html')

@main_blueprint.route('/profile')
@login_required
def profile():
    return f"Привет, {current_user.email}! Это твой профиль."
