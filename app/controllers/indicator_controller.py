from flask import Blueprint, request, jsonify
from app.service.indicator_service import create_indicator, get_all_indicators, assign_coordinator_to_indicator, remove_coordinator_from_indicator, count_indicators, get_indicators_by_username, get_indicator_assignments
from app.middleware.middleware import role_required, jwt_required

indicator_bp = Blueprint('indicators', __name__)

@indicator_bp.route('/indicators', methods=['POST'])
@role_required(['Administrador' ])
def create_indicato():
    try:
        data = request.json
        print("Datos recibidos en el POST /indicators:", data)
        indicator = create_indicator(data)
        print(indicator)
        return jsonify({
            'id': indicator.id,
            'name': indicator.name,
            'delivery_deadline': indicator.delivery_deadline,
            'due_date': indicator.due_date,
            'improvement_action': indicator.improvement_action,
            'expected_result': indicator.expected_result,
            'academic_objective_id': indicator.academic_objective_id,
            'sgc_objective_id': indicator.sgc_objective_id,
            'formula_id': indicator.formula_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@indicator_bp.route('/indicators', methods=['GET'])
@jwt_required()  
@role_required(['Administrador', 'director'])
def get_indicators():
    try:
        indicators = get_all_indicators()
        result = []
        for indicator in indicators:
            result.append({
                'id': indicator.id,
                'name': indicator.name,
                'delivery_deadline': str(indicator.delivery_deadline),
                'due_date': str(indicator.due_date),
                'improvement_action': indicator.improvement_action,
                'expected_result': indicator.expected_result,
                'academic_objective': indicator.academic_objective.name if indicator.academic_objective else None,
                'sgc_objective': indicator.sgc_objective.name if indicator.sgc_objective else None,
                'formula': indicator.formula.formula if indicator.formula else None
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@indicator_bp.route('/indicators/<int:indicator_id>/assign-coordinator', methods=['POST'])
def assign_coordinator(indicator_id):
    try:
        data = request.json
        print(f"Datos recibidos en POST /indicators/{indicator_id}/assign-coordinator:", data)
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'error': 'user_id es obligatorio'}), 400

        result = assign_coordinator_to_indicator(indicator_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@indicator_bp.route('/indicators/<int:indicator_id>/remove-coordinator', methods=['DELETE'])
def remove_coordinator(indicator_id):
    try:
        data = request.json
        print(f"Datos recibidos en DELETE /indicators/{indicator_id}/remove-coordinator:", data)
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'error': 'user_id es obligatorio'}), 400

        result = remove_coordinator_from_indicator(indicator_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@indicator_bp.route('/indicators/simple', methods=['GET'])
def get_indicators_with_coordinators():
    try:
        indicators = get_all_indicators()
        result = []
        for indicator in indicators:
            coordinators = [{
                'id': user.id,
                'username': user.username,
                'name': user.name
            } for user in indicator.users]  

            result.append({
                'id': indicator.id,
                'name': indicator.name,
                'coordinators': coordinators
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@indicator_bp.route('/indicators/count', methods=['GET'])
def get_indicator_counts():
    try:
        counts = count_indicators()
        return jsonify(counts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
  
    
@indicator_bp.route('/indicators/user/<string:username>', methods=['GET'])
def get_indicators_by_user(username):
    try:
        indicators = get_indicators_by_username(username)
        return jsonify(indicators), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@indicator_bp.route('/indicators/assignments', methods=['GET'])
def get_all_assignments():
    """Endpoint para obtener todas las asignaciones de indicadores"""
    try:
        assignments = get_indicator_assignments()
        return jsonify(assignments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

