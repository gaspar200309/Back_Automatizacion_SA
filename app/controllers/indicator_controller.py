from flask import Blueprint, request, jsonify
from app.service.indicator_service import IndicatorService
from app.middleware.middleware import role_required, jwt_required

indicator_bp = Blueprint('indicators', __name__)

@indicator_bp.route('/indicators', methods=['POST'])
@jwt_required()  
@role_required(['Administrador'])
def create_indicator():
    data = request.json
    print("Datos recibidos en el POST /indicators:", data)
    try:
        indicator = IndicatorService.create_indicator(data)
        return jsonify(indicator), 201
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400

@indicator_bp.route('/indicators', methods=['GET'])
#@jwt_required()  
#@role_required(['Administrador'])
def get_indicators():
    try:
        indicators = IndicatorService.get_all_indicators()
        return jsonify(indicators), 200  # Evitar reprocesar datos
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@indicator_bp.route('/indicators/<int:indicator_id>/assign-coordinator', methods=['POST'])
@jwt_required()
@role_required(['Administrador'])
def assign_coordinator(indicator_id):
    try:
        data = request.json
        print(f"Datos recibidos en POST /indicators/{indicator_id}/assign-coordinator", data)
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'error': 'user_id es obligatorio'}), 400

        result = IndicatorService.assign_coordinator(indicator_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@indicator_bp.route('/indicators/<int:indicator_id>/remove-coordinator', methods=['DELETE'])
@jwt_required()
@role_required(['Administrador'])
def remove_coordinator(indicator_id):
    try:
        data = request.json
        print(f"Datos recibidos en DELETE /indicators/{indicator_id}/remove-coordinator:", data)
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'error': 'user_id es obligatorio'}), 400

        result = IndicatorService.remove_coordinator(indicator_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@indicator_bp.route('/indicators/simple', methods=['GET'])
@jwt_required()
@role_required(['Administrador', 'director', 'coordinador'])
def get_indicators_with_coordinators():
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        indicators = IndicatorService.get_all_indicators(limit=limit, offset=offset)
        return jsonify(indicators), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@indicator_bp.route('/indicators/count', methods=['GET'])
@jwt_required()
@role_required(['Administrador', 'director', 'coordinador'])
def get_indicator_counts():
    try:
        counts = IndicatorService.count_indicators()
        return jsonify(counts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@indicator_bp.route('/indicators/user/<string:username>', methods=['GET'])
@jwt_required()
@role_required(['Administrador', 'director', 'coordinador'])
def get_indicators_by_user(username):
    try:
        indicators = IndicatorService.get_indicators_by_username(username)
        if not indicators:
            return jsonify({'message': 'No indicators found for user'}), 404
        return jsonify(indicators), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@indicator_bp.route('/indicators/assignments', methods=['GET'])
@jwt_required()
def get_all_assignments():
    try:
        assignments = IndicatorService.get_indicator_assignments()
        return jsonify(assignments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@indicator_bp.route('/indicators/deadlines', methods=['GET'])
@jwt_required()
@role_required(['Administrador'])
def get_indicator_deadlines():
    try:
        deadlines = IndicatorService.get_indicator_deadlines_service()
        return jsonify(deadlines), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@indicator_bp.route('/indicators/<int:indicator_id>/users', methods=['GET'])
def get_assigned_users(indicator_id):
    try:
        users = IndicatorService.get_assigned_users_by_indicator(indicator_id)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

