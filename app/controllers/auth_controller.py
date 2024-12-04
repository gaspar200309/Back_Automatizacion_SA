from flask import Blueprint, request, jsonify
from app.service.auth_service import create_user, authenticate_user
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json if request.is_json else request.form
        print("Datos recibidos en POST /register:", data)

        # Validar campos requeridos
        required_fields = ['username', 'name', 'last_name', 'email', 'password', 'role']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"error": f"Faltan los campos requeridos: {', '.join(missing_fields)}"}), 400

        # Extraer datos
        username = data.get('username')
        name = data.get('name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role')
        phone = data.get('phone', None)
        photo = request.files.get('photo', None)

        # Crear usuario
        user, message = create_user(username, name, last_name, email, password, role_id, phone, photo)
        if user:
            return jsonify({"message": message}), 201

        return jsonify({"error": message}), 400

    except Exception as e:
        import traceback
        print("Error en /register:", traceback.format_exc())
        return jsonify({"error": "Error inesperado en el servidor."}), 500

    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('identifier')
    password = data.get('password')

    user, message = authenticate_user(identifier, password)

    if user and hasattr(user, 'id') and user.roles and hasattr(user.roles[0].role, 'name'):
        role_name = user.roles[0].role.name
        access_token = create_access_token(identity=user.id, additional_claims={"role": role_name})
        photo_url = user.photo if hasattr(user, 'photo') else None
        
        # Concatenando nombre y apellido
        full_name = f"{user.name} {user.last_name}"
        
        return jsonify({
            "access_token": access_token,
            "username": user.username,
            "full_name": full_name,  
            "roles": role_name,
            "photo": photo_url,
            "phone": user.phone,
            "message": "Login successful"
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401



