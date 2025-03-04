from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from backend import app, db
from backend.models import User


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': '用户已存在'}), 400
    passw_hash = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=passw_hash)  
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter(User.username == data['username']).first()

    if check_password_hash(user.password, data['password']):
        return jsonify({'message': '登录成功'})
    return jsonify({'message': '无效凭证'}), 401