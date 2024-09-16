from flask import Blueprint, request, jsonify
from app.service.indicator_service import create_indicator, get_all_indicators

indicator_bp = Blueprint('indicators', __name__)

@indicator_bp.route('/indicators', methods=['POST'])
def create_indicato():
    try:
        data = request.json
        indicator = create_indicator(data)
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
