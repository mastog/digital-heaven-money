from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from backend import app, db
from backend.models import User


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'user exist'}), 400
    passw_hash = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=passw_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'success'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter(User.username == data['username']).first()

    if check_password_hash(user.password, data['password']):
        return jsonify({'message': 'success'})
    return jsonify({'message': 'wrong password or username'}), 401