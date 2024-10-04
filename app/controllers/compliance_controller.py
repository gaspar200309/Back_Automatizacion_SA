
from flask import Blueprint, request, jsonify
from app.service.compliance_service import get_evaluations_by_indicator, get_evaluation_statistics, create_new_evaluation, get_all_evaluations_with_details, create_new_evaluation_with_trimester, get_all_with_details_indicator4


compliance_bp = Blueprint('compliance_bp', __name__)

@compliance_bp.route('/evaluations', methods=['POST'])
def create_evaluation_route():
    data = request.json
    try:
        evaluation = create_new_evaluation(
            data['indicator_id'],
            data['teacher_id'],
            data['state_id']
        )
        return jsonify({'message': 'Evaluation created successfully', 'id': evaluation.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    

@compliance_bp.route('/evaluations/<int:indicator_id>', methods=['GET'])
def get_evaluations(indicator_id):
    evaluations = get_evaluations_by_indicator(indicator_id)
    return jsonify([{
        'id': e.id,
        'teacher_name': f"{e.teacher.name} {e.teacher.last_name}",
        'state': e.state.name
    } for e in evaluations])

@compliance_bp.route('/evaluations/<int:indicator_id>/statistics', methods=['GET'])
def get_evaluation_statistics(indicator_id):
    stats = get_evaluation_statistics(indicator_id)
    return jsonify(stats)

@compliance_bp.route('/evaluations/all/<int:indicator_id>', methods=['GET'])
def get_all_evaluations(indicator_id):
    evaluations, statistics = get_all_evaluations_with_details(indicator_id)
    return jsonify({
        'evaluations': evaluations,
        'statistics': statistics
    })
    
@compliance_bp.route('/evaluations/indicator4', methods=['POST'])
def create_evaluation_with_trimester_route():
    data = request.json
    try:
        evaluation = create_new_evaluation_with_trimester(
            data['indicator_id'],
            data['teacher_id'],
            data['trimestre_id'],
            data['state_id'],
        )
        return jsonify({'message': 'Evaluación creada exitosamente', 'id': evaluation.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    
@compliance_bp.route('/evaluations/indicator4/<int:indicator_id>', methods=['GET'])
def get_all_evaluations_indicator4(indicator_id):
    evaluations, statistics = get_all_with_details_indicator4(indicator_id)
    return jsonify({
        'evaluations': evaluations,
        'statistics': statistics
    })
