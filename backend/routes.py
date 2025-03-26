import os
import time
from datetime import datetime,date
import secrets
import string
import random

from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename

from backend import app
from backend.models.DAOs import dao_factory

# User Management
from backend.services import aiService
from backend.services.lunarCalendarService import get_lunarCalendar
from backend.services.utils import allowed_file


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    user = dao_factory.get_dao("User").get(username=data.get('username'))
    if user:
        return jsonify({'error': 'User already registered'}), 409
    dao_factory.get_dao("User").create(**data)
    return jsonify({'message': 'Success'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    user = dao_factory.get_dao("User").get(username=data.get('username'))
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200

@app.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = dao_factory.get_dao("User").get(id=current_user_id)
    if request.method == 'GET':
        return jsonify(user.to_dict()), 200
    elif request.method == 'PUT':
        data = request.get_json()
        updated_user = dao_factory.get_dao("User").update(user, **data)
        return jsonify(updated_user.to_dict()), 200

# Data Management (CRUD)
@app.route('/crud/<resource>', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required()
def data_management(resource):
    dao=dao_factory.get_dao(resource)
    if not dao:
        return jsonify({'error': 'Resource not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if request.method == 'POST':
        return jsonify(dao.create(**data).to_dict()),200

    elif request.method == 'PUT':
        if not data.get('id') or not dao.get(id=data.get('id')):
            return jsonify({'error': 'item not found'}), 400
        return jsonify(dao.update(dao.get(id=data.get('id')),**data).to_dict()),200

    elif request.method == 'GET':
        return jsonify([obj.to_dict() for obj in dao.get_all(**data)]),200

    else:
        if not data.get('id') or not dao.get(id=data.get('id')):
            return jsonify({'error': 'item not found'}), 400
        dao.delete(dao.get(id=data.get('id')))
        return jsonify({'success': True}), 200


# Invite Users to Memorial Hall
@app.route('/memorial/<int:id>/invite', methods=['POST'])
@jwt_required()
def invite_users(id):  # memorial id
    current_user_id = get_jwt_identity()
    alphabet = string.ascii_letters + string.digits  # Contains letters and numbers
    invite_key = ''.join(secrets.choice(alphabet) for _ in range(16))  # Generates a 16-bit random invitation code
    data = {'user_id': current_user_id,
            'deceased_id': id,
            'key': invite_key}
    dao_factory.get_dao("InviteKey").create(**data)
    return jsonify({'invite_key': invite_key}), 201

@app.route('/ai', methods=['POST'])
@jwt_required()
def ai_request():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    response=aiService.connect(data.get('text'))
    return jsonify({'response': response}), 201

@app.route('/dailyQuestion', methods=['GET'])
def daily_question():
    random.seed(date.today())  #The same date generates the same random number
    id_today=random.randint(1, 60)
    return jsonify(dao_factory.get_dao("DailyQuestion").get({id==id_today}).to_dict()), 200

@app.route('/history', methods=['GET'])
def history():
    current_month = datetime.now().month
    current_day = datetime.now().day

    history_objects = dao_factory.get_dao("history").get_all(month=current_month, day=current_day)
    result=[]
    for obj in history_objects:
        url="https://en.wikipedia.org/wiki/"+obj.name
        obj_dict = obj.to_dict()
        #  Add url key-value pairs
        obj_dict["url"] = url
        result.append(obj_dict)

    return jsonify(result), 200


@app.route('/lunar', methods=['GET'])
def lunarCalendar():
    return jsonify(get_lunarCalendar(datetime.now())), 200

@app.route('/upload_pic', methods=['POST'])
def upload_pic():
    if 'pic' not in request.files:
        return jsonify({'error': 'No picture part'}), 400

    file = request.files['pic']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        name, ext = os.path.splitext(filename)
        # Add a timestamp to the file name
        timestamped_filename = f"{name}_{int(time.time())}{ext}"

        file_path = os.path.join(app.config['FILE_UPLOAD_DIR'], timestamped_filename)
        file.save(file_path)  # save the picture

        return jsonify({'message': 'Picture uploaded successfully','pic_name': timestamped_filename}), 200

    return jsonify({'error': 'Invalid file type'}), 400

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500