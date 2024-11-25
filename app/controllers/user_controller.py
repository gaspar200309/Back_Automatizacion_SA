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
            'roles': [role.role.name for role in user.roles],
            'photo': user.photo,
            'phone' : user.phone
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
def get_user_by_id(user_id):
    user_data = UserService.get_user_by_id(user_id)
    if user_data:
        return jsonify(user_data)
    return jsonify({'error': 'User not found'}), 404



@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.form
    photo = request.files.get('photo') 

    updated_user = UserService.update_user(
        user_id, 
        data['username'], 
        data['name'], 
        data['last_name'], 
        data['email'], 
        data.getlist('role'),  
        data['phone'],
        photo
    )
    if updated_user:
        return jsonify({
            'id': updated_user.id, 
            'name': updated_user.name, 
            'last_name': updated_user.last_name, 
            'username': updated_user.username, 
            'email': updated_user.email,
            'photo': updated_user.photo,
            'phone': updated_user.phone
        })
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users/count', methods=['GET'])
def count_users():
    user_count = UserService.get_user_count()
    return jsonify({'total_users': user_count})

