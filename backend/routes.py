from flask import Flask, request, jsonify, redirect
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from backend import app
from backend.DAOs import dao_factory

# User Management
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
def invite_users(id):
    data = request.get_json()
    invite_link = dao_factory.get_dao("InviteKey").create(**data)
    return jsonify({'invite_link': invite_link.key}), 201



# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500