from flask import Blueprint, jsonify, render_template, request, send_file
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from .models import User, TransposeHistory, db, PLAN_LIMITS
import uuid
import os
from .utils import check_usage_limit
from .transpose import transpose_file

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/api/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"username": user.username, "plan": user.plan})

@routes_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

#@routes_bp.route('/login', methods=['GET'])
#def login_page():
    #return render_template('login.html')

@routes_bp.route('/api/transpose', methods=['POST'])
@jwt_required()
def transpose():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not check_usage_limit(user):
        return jsonify({"msg": "Usage limit exceeded for your plan"}), 429

    # TODO: здесь вызываем твою функцию транспонирования...
    # transposed_result = your_transpose_function(...)

    # Увеличиваем счётчик
    user.usage_today += 1
    db.session.commit()

    return jsonify({"msg": "Transposition successful"})


@routes_bp.route('/api/upgrade', methods=['POST'])
@jwt_required()
def upgrade_plan():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()

    if data['plan'] not in PLAN_LIMITS:
        return jsonify({"msg": "Invalid plan"}), 400

    user.plan = data['plan']
    db.session.commit()
    return jsonify({"msg": f"Upgraded to {user.plan}!"})


@routes_bp.route('/api/transpose/file', methods=['POST'])
@jwt_required()
def transpose_file_route():
    print(request, request.files)
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not check_usage_limit(user):
        return jsonify({"msg": "Usage limit exceeded for your plan"}), 429

    if 'file' not in request.files:
        return jsonify({'msg': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'msg': 'No selected file'}), 400

    semitones = request.form.get('semitones', default='0')
    try:
        semitones = int(semitones)
    except ValueError:
        return jsonify({'msg': 'Invalid semitones value'}), 400

    filename = secure_filename(file.filename)
    uid = str(uuid.uuid4())
    ext = os.path.splitext(filename)[1].lower()

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'{uid}_{filename}')
    file.save(upload_path)

    try:
        if ext in ['.mid', '.midi', '.xml', '.musicxml', '.png', '.jpg', '.jpeg']:
            png_path, pdf_path = transpose_file(upload_path, uid, semitones, current_app.config['RESULT_FOLDER'])
        else:
            return jsonify({'msg': f'Unsupported file type: {ext}'}), 400
    except Exception as e:
        print(e)
        return jsonify({'msg': f'Failed to process file: {str(e)}'}), 500

    # Обновляем историю пользователя
    user.usage_today += 1
    db.session.commit()

    # Возвращаем пути
    return jsonify({
        'png_url': f'/api/transpose/image/{uid}',
        'pdf_url': f'/api/transpose/pdf/{uid}'
    })


@routes_bp.route('/api/transpose/image/<uid>')
@jwt_required()
def get_png(uid):
    path = os.path.join(current_app.config['RESULT_FOLDER'], f'{uid}.png')
    if not os.path.exists(path):
        return jsonify({'msg': 'Image not found'}), 404
    return send_file(path, mimetype='image/png')

@routes_bp.route('/api/transpose/pdf/<uid>')
@jwt_required()
def get_pdf(uid):
    path = os.path.join(current_app.config['RESULT_FOLDER'], f'{uid}.pdf')
    if not os.path.exists(path):
        return jsonify({'msg': 'PDF not found'}), 404
    return send_file(path, mimetype='application/pdf', as_attachment=True)
