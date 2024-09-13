from flask import Blueprint, request, jsonify
from app.service.auth_service import create_user, authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(data)
        username = data.get('username')
        name = data.get('name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role') 

        user, message = create_user(username, name, last_name, email, password, role_id)
        if user:
            return jsonify({"message": message}), 201
        return jsonify({"error": message}), 400
    except Exception as e:
        print(f"Error in register route: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    identifier = data.get('identifier')  
    password = data.get('password')

    auth_response, message = authenticate_user(identifier, password)
    if auth_response:
        return jsonify(auth_response), 200
    return jsonify({"error": message}), 401

