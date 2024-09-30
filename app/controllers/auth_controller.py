from flask import Blueprint, request, jsonify
from app.service.auth_service import create_user, authenticate_user
from flask_jwt_extended import create_access_token, set_access_cookies


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
    data = request.json
    identifier = data.get('identifier')
    password = data.get('password')

    user, message = authenticate_user(identifier, password)

    if user and hasattr(user, 'id') and user.roles and hasattr(user.roles[0].role, 'name'):
        role_name = user.roles[0].role.name
        access_token = create_access_token(identity=user.id, additional_claims={"role": role_name})
        # photo_url = user.photo_url if hasattr(user, 'photo_url') else None
        
        return jsonify({
            "access_token": access_token,
            "username": user.username,
            "roles": role_name,
            # "photo": photo_url  # Descomentar cuando la propiedad 'photo_url' esté disponible
            "message": "Login successful"
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401



