
from flask import Blueprint, request, jsonify
from app.service.compliance_service import get_evaluations_by_indicator, get_evaluation_statistics, create_new_evaluation, get_all_evaluations_with_details, create_new_evaluation_with_trimester, get_all_with_details_indicator4, create_indicator6_evaluation_service, get_estadistic_indicator6, create_new_evaluation_with_period, get_all_with_details_indicator7, create_indicator8_period, get_all_with_details_indicator8, get_statistics_by_trimester_and_indicator, get_estadistic_indicator6_by_period


compliance_bp = Blueprint('compliance_bp', __name__)

@compliance_bp.route('/evaluations/indicator2', methods=['POST'])
def create_evaluation_route():
    data = request.json
    try:
        evaluation = create_new_evaluation(
            data['indicator_id'],
            data['teacher_id'],
            data['state_id']
        )
        return jsonify({'success': True, 'message': 'Evaluation created successfully', 'id': evaluation.id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

    
    
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
    
@compliance_bp.route('/evaluations/indicator4/<int:indicator_id>/<int:trimestre_id>', methods=['GET'])
def get_evaluations_by_trimester(indicator_id, trimestre_id):
    statistics = get_statistics_by_trimester_and_indicator(indicator_id, trimestre_id)
    return jsonify({
        'statistics': statistics
    })

    
@compliance_bp.route('/create_indicator6', methods=['POST'])
def create_indicator6_evaluation():
    data = request.get_json()
    print(data)
    if not data or not isinstance(data, list):
        return jsonify({'error': 'Se requiere un arreglo de datos', 'status': 400}), 400

    try:
        result = create_indicator6_evaluation_service(data)
        return jsonify(result), result['status']
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500

   

@compliance_bp.route('/evaluations/indicator6/<int:indicator_id>', methods=['GET'])
def get_indicator6_stats(indicator_id):
    try:
        stats = get_estadistic_indicator6(indicator_id)
        return jsonify(stats), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@compliance_bp.route('/evaluations/indicator6/<int:indicator_id>/<int:period_id>', methods=['GET'])
def get_indicator6_stats2(indicator_id, period_id):
    try:
        if not isinstance(indicator_id, int) or not isinstance(period_id, int):
            return jsonify({"error": "Parámetros inválidos"}), 400

        stats = get_estadistic_indicator6_by_period(indicator_id, period_id)

        if not stats:
            return jsonify({"message": "No se encontraron datos"}), 404

        return jsonify({'statistics': stats}), 200
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    
@compliance_bp.route('/evaluations/indicator7', methods=['POST'])
def create_evaluation_with_period_route():
    data = request.json
    try:
        evaluation = create_new_evaluation_with_period(
            data['indicator_id'],
            data['teacher_id'],
            data['period_id'],
            data['state_id'],
        )
        return jsonify({'message': 'Evaluación creada exitosamente', 'id': evaluation.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@compliance_bp.route('/evaluations/indicator7/<int:indicator_id>', methods=['GET'])
def get_all_evaluations_indicator7(indicator_id):
    evaluations, statistics = get_all_with_details_indicator7(indicator_id)
    return jsonify({
        'evaluations': evaluations,
        'statistics': statistics
    })
    
@compliance_bp.route('/evaluations/indicator8', methods=['POST'])
def create_indicator8_cont():
    data = request.json
    try:
        evaluation = create_indicator8_period(
            data['indicator_id'],
            data['teacher_id'],
            data['period_id'],
            data['state_id'],
        )
        return jsonify({'message': 'Evaluación creada exitosamente', 'id': evaluation.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@compliance_bp.route('/evaluations/indicator8/<int:indicator_id>', methods=['GET'])
def get_all_evaluations_indicator8(indicator_id):
    evaluations, statistics = get_all_with_details_indicator8(indicator_id)
    return jsonify({
        'evaluations': evaluations,
        'statistics': statistics
    })
 
    
