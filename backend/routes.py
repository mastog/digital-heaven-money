import os
import time
from datetime import datetime, date
import secrets
import string
import random

from flask import request, jsonify, session
from werkzeug.utils import secure_filename

from backend import app, login_manager
from backend.models.DAOs import dao_factory

# User Management
from backend.services import aiService
from backend.services.lunarCalendarService import get_lunarCalendar
from backend.services.utils import allowed_file, picUpdate
from flask_login import login_user, logout_user, login_required, current_user

# 用户加载器回调
@login_manager.user_loader
def load_user(user_id):
    user_dao = dao_factory.get_dao("User")
    return user_dao.get(id=user_id)


@login_manager.unauthorized_handler
def handle_unauthorized():
    from flask import request, jsonify, redirect

    if request.accept_mimetypes.accept_json:
        return jsonify({
            "error": "Unauthorized",
            "code": 401,
            "redirect": "/login"  # 可选：携带重定向地址
        }), 401
    # 否则返回重定向（传统浏览器请求）
    return redirect("/login")

@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    user = dao_factory.get_dao("User").get(username=data.get('username'))
    if user:
        return jsonify({'error': 'User already registered'}), 409
    dao_factory.get_dao("User").create(**data)
    return jsonify({'message': 'Success'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    user = dao_factory.get_dao("User").get(username=data.get('username'))
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    login_user(user)  # 使用flask_login的login_user函数登录用户
    print(current_user.to_dict())
    return jsonify({'message': user.username+' login successful'}), 200


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    name = current_user.username
    logout_user()  # 使用flask_login的logout_user函数登出用户
    return jsonify({'message': name+' logout successful'}), 200


@app.route('/current', methods=['POST'])
def current():
    if not current_user.is_authenticated:
        return jsonify(None), 200  # 返回 `null`（JSON 里的 None）
    return jsonify(current_user.to_dict()), 200


@app.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    user = current_user
    if request.method == 'GET':
        return jsonify(user.to_dict()), 200
    elif request.method == 'PUT':
        data = request.form.to_dict()
        if 'pic' in request.files:
            filename = picUpdate(request)
            data['pic_url'] = filename
        updated_user = dao_factory.get_dao("User").update(user, **data)
        return jsonify(updated_user.to_dict()), 200


@app.route('/crud/<resource>/<action>', methods=['POST'])
def data_management(resource, action):
    dao = dao_factory.get_dao(resource)
    if not dao:
        return jsonify({'error': 'Resource not found'}), 404

    data = request.form.to_dict()
    if 'pic' in request.files:
        filename = picUpdate(request)
        data['pic_url'] = filename

    if 'id' in data:
        try:
            data['id'] = int(data['id'])
        except ValueError:
            return jsonify({'error': 'Invalid id format'}), 400

    if action == 'create':
        return jsonify(dao.create(**data).to_dict()), 200

    elif action == 'update':
        obj = dao.get(id=data.get('id'))
        if not obj:
            return jsonify({'error': 'Item not found'}), 400
        return jsonify(dao.update(obj, **data).to_dict()), 200

    elif action == 'get':
        return jsonify([obj.to_dict() for obj in dao.get_all(**data)]), 200

    elif action == 'delete':
        obj = dao.get(id=data.get('id'))
        if not obj:
            return jsonify({'error': 'Item not found'}), 400
        dao.delete(obj)
        return jsonify({'success': True}), 200

    else:
        return jsonify({'error': f'Unknown action "{action}"'}), 400


# Invite Users to Memorial Hall
@app.route('/invite/<int:id>', methods=['GET'])
@login_required
def invite_users(id):  # memorial id
    current_user_id = current_user.id
    message = "The invitation code has been created. "
    exist = dao_factory.get_dao("InviteKey").get({'user_id': current_user_id, 'deceased_id': id})
    if exist:
        dao_factory.get_dao("InviteKey").delete(exist)
        message += "The previous invitation code has been overwritten"
    alphabet = string.ascii_letters + string.digits  # Contains letters and numbers
    invite_key = ''.join(secrets.choice(alphabet) for _ in range(16))  # Generates a 16-bit random invitation code
    data = {'user_id': current_user_id,
            'deceased_id': id,
            'key': invite_key}
    dao_factory.get_dao("InviteKey").create(**data)
    return jsonify({'invite_key': invite_key, 'message': message}), 201


# Join in Memorial Hall
@app.route('/join/<string:key>', methods=['GET'])
@login_required
def join(key):  # memorial id
    current_user_id = current_user.id
    inviteDao = dao_factory.get_dao("InviteKey")
    invite = inviteDao.get({"key": key})
    if not invite:
        return jsonify({'error': "Unrecognizable key"}), 400
    if invite.user.id == current_user_id:
        return jsonify({'error': "Why do you use the invitation code you created to invite yourself?"}), 400
    if current_user_id == invite.deceased.creator_id:
        return jsonify({'error': "You cannot join the memorial you created yourself again"}), 400
    if dao_factory.get_dao("DeceasedUser").get({"deceased_id": invite.deceased.id, "user_id": current_user_id}):
        return jsonify({'error': "You have joined this memorial"}), 400
    data = {'user_id': current_user_id,
            'deceased_id': invite.deceased.id
            }
    dao_factory.get_dao("DeceasedUser").create(**data)
    return jsonify({'message': "You joined " + invite.deceased.name + "'s memorial at " + invite.user.username + "'s invitation"}), 201


@app.route('/ai', methods=['POST'])
def ai_request():
    data = request.form.to_dict()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    response = aiService.communicate(data.get('name'), data.get('description'), data.get('text'))
    return jsonify({'response': response}), 201


@app.route('/dailyQuestion', methods=['GET'])
def daily_question():
    random.seed(str(date.today()))  # The same date generates the same random number
    daily_questions = dao_factory.get_dao("DailyQuestion").get_all()
    id_today = random.randint(0, len(daily_questions) - 1)
    # Transform the data into the desired format
    formatted_question = {
        "question": daily_questions[id_today].question,
        "options": {
            "a": daily_questions[id_today].answerA,
            "b": daily_questions[id_today].answerB,
            "c": daily_questions[id_today].answerC,
            "d": daily_questions[id_today].answerD
        },
        "correctAnswer": daily_questions[id_today].correctAnswer.lower(),  # Ensure it's lowercase
        "explanation": daily_questions[id_today].explanation
    }

    return jsonify(formatted_question), 200


@app.route('/history', methods=['GET'])
def history():
    current_month = datetime.now().month
    current_day = datetime.now().day

    history_objects = dao_factory.get_dao("History").get_all(month=current_month, day=current_day)
    result = []
    for obj in history_objects:
        obj_dict = obj.to_dict()
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

        return jsonify({'message': 'Picture uploaded successfully', 'pic_name': timestamped_filename}), 200

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/publicDeceased', methods=['GET'])
def public_deceased():
    dao = dao_factory.get_dao("Deceased")
    return jsonify([obj.to_dict() for obj in dao.get_all({"is_private": False})]), 200


@app.route('/privateDeceased', methods=['GET'])
@login_required
def private_deceased():
    current_user_id = current_user.id
    result = getPrivateMemorial(current_user_id)
    return jsonify([obj.to_dict() for obj in result]), 200


@app.route('/timeLine/<int:id>', methods=['GET'])
def get_timeLine(id):
    dao = dao_factory.get_dao("DeceasedPhoto")
    timeLine = dao.get_all({"deceased_id": id})
    timeLine = sorted(timeLine, key=lambda x: x['photo_date'])
    return jsonify([obj.to_dict() for obj in timeLine]), 200


@app.route('/keys', methods=['GET'])
def get_keys():
    return jsonify(dao_factory.get_dao_keys()), 200


# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


def getPrivateMemorial(current_user_id):
    deceasedDao = dao_factory.get_dao("Deceased")
    joinedDao = dao_factory.get_dao("DeceasedUser")
    result = deceasedDao.get_all({"is_private": False, "creator_id": current_user_id})
    for i in joinedDao.get_all({"user_id": current_user_id}):
        result.append(i.deceased)
    return result