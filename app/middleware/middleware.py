from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from functools import wraps
from flask import jsonify

def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        @jwt_required() 
        def wrapper(*args, **kwargs):
            claims = get_jwt() 
            user_role = claims.get('role')

            if user_role not in required_roles:
                return jsonify({"error": "Access denied, insufficient permissions"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
