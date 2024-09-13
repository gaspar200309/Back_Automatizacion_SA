from flask import Blueprint, request, jsonify
from app.service.user_service import UserService

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return jsonify([
        {
            'id': user.id,
            'name': user.name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'roles': [role.role.name for role in user.roles]  
        } for user in users
    ])

@user_bp.route('/roles', methods=['GET'])
def get_roles():
    roles = UserService.get_all_roles()
    return jsonify([
        {
            'id': role.id,
            'name': role.name
        } for role in roles
    ])



@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify({
            'id': user.id, 
            'name': user.name, 
            'last_name': user.last_name, 
            'username': user.username, 
            'email': user.email
        })
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    print(data)
    new_user = UserService.create_user(
        username=data['username'], 
        name=data['firstName'],  
        last_name=data['lastName'],
        email=data['email'], 
        password=data['password'], 
        role_ids=data['role_ids']
    )
    return jsonify({
        'id': new_user.id, 
        'name': new_user.name, 
        'last_name': new_user.last_name, 
        'username': new_user.username, 
        'email': new_user.email
    }), 201



@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    updated_user = UserService.update_user(
        user_id, 
        data['username'], 
        data['name'], 
        data['last_name'], 
        data['email'], 
        data['role']
    )
    if updated_user:
        return jsonify({
            'id': updated_user.id, 
            'name': updated_user.name, 
            'last_name': updated_user.last_name, 
            'username': updated_user.username, 
            'email': updated_user.email
        })
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404
