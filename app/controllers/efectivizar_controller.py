from flask import Blueprint, request, jsonify
from app.service.efectivizar_service import StudentStatusService

student_status_bp = Blueprint('student_status_bp', __name__)

@student_status_bp.route('/register_active_students', methods=['POST'])
def register_active_students():
    data = request.get_json()
    trimestre_id = data.get('trimestre_id')
    active_students_count = data.get('active_students')

    if not trimestre_id or active_students_count is None:
        return jsonify({"error": "Trimestre ID y cantidad de estudiantes activos son requeridos"}), 400

    # Llama al servicio para registrar estudiantes activos
    result = StudentStatusService.register_active_students(trimestre_id, active_students_count)
    return jsonify(result), 201

@student_status_bp.route('/get_student_status/<int:trimestre_id>', methods=['GET'])
def get_student_status(trimestre_id):
    result = StudentStatusService.get_student_status(trimestre_id)
    if not result:
        return jsonify({"error": "No se encontró el estado para el trimestre especificado"}), 404

    return jsonify(result), 200

@student_status_bp.route('/get_all_student_statuses', methods=['GET'])
def get_all_student_statuses():
    result = StudentStatusService.get_all_student_statuses()
    return jsonify(result), 200


@student_status_bp.route('/register-license', methods=['POST'])
def register_license():
    data = request.get_json()
    print(data)
    required_fields = ["indicator_id", "trimestre_id", "course_id", "licencia"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    response, status = StudentStatusService.register_licenses(
        indicator_id=data["indicator_id"],
        trimestre_id=data["trimestre_id"],
        course_id=data["course_id"],
        licencia=data["licencia"],
    )
    return jsonify(response), status

@student_status_bp.route('/statistics/course/<int:course_id>', methods=['GET'])
def get_statistics_by_course(course_id):
    stats = StudentStatusService.get_statistics_by_course(course_id)
    return jsonify(stats), 200

@student_status_bp.route('/statistics/trimester/<int:trimestre_id>', methods=['GET'])
def get_statistics_by_trimester(trimestre_id):
    stats = StudentStatusService.get_statistics_by_trimester(trimestre_id)
    return jsonify(stats), 200

@student_status_bp.route('/statistics/general', methods=['GET'])
def get_general_statistics():
    stats = StudentStatusService.get_detailed_statistics()
    return jsonify(stats), 200

@student_status_bp.route('/register-insidence', methods=['POST'])
def register_incidences():
    data = request.get_json()
    print(data)
    response = StudentStatusService.register_incidences(data)
    return jsonify(response), 201


@student_status_bp.route('/statistics', methods=['GET'])
def get_incidences_statistics():
    course_id = request.args.get('course_id', type=int)
    trimester_id = request.args.get('trimester_id', type=int)
    semester_id = request.args.get('semester_id', type=int)

    stats = StudentStatusService.get_incidences_statistics(
        course_id=course_id,
        trimester_id=trimester_id,
        semester_id=semester_id
    )

    return jsonify(stats), 200

@student_status_bp.route('/registro-nota', methods=['POST'])
def register_nota_status():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400

    required_fields = ['indicator_id', 'course_id', 'teacher_id', 'state_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"El campo {field} es requerido"}), 400

    response, status_code = StudentStatusService.register_nota_status(data)
    return jsonify(response), status_code

@student_status_bp.route('/registro-nota', methods=['GET'])
def get_nota_status():
    """
    Endpoint para obtener estados de notas
    """
    filters = {
        'indicator_id': request.args.get('indicator_id', type=int),
        'trimestre_id': request.args.get('trimestre_id', type=int),
        'course_id': request.args.get('course_id', type=int),
        'period_id': request.args.get('period_id', type=int),
        'teacher_id': request.args.get('teacher_id', type=int)
    }
    # Eliminar filtros None
    filters = {k: v for k, v in filters.items() if v is not None}

    response, status_code = StudentStatusService.get_nota_status(filters)
    return jsonify(response), status_code

@student_status_bp.route('/registro-nota/statistics', methods=['GET'])
def get_statistics():
    """
    Endpoint para obtener estadísticas de estados de notas
    """
    filters = {
        'indicator_id': request.args.get('indicator_id', type=int),
        'trimestre_id': request.args.get('trimestre_id', type=int),
        'period_id': request.args.get('period_id', type=int)
    }
    # Eliminar filtros None
    filters = {k: v for k, v in filters.items() if v is not None}

    response, status_code = StudentStatusService.get_statistics(filters)
    return jsonify(response), status_code

# Registrar comunicados
@student_status_bp.route('/register-communication', methods=['POST'])
def register_communication():
    data = request.get_json()
    print(data)
    required_fields = ["indicator_id", "trimestre_id", "course_id", "communication"]

    # Revisar solo los campos estrictamente necesarios
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Registrar el comunicado
    response = StudentStatusService.register_communications(data)
    return jsonify(response), 201

@student_status_bp.route('/communication-statistics', methods=['GET'])
def get_communication_statistics():
    course_id = request.args.get('course_id', type=int)
    trimestre_id = request.args.get('trimestre_id', type=int)

    stats = StudentStatusService.get_communication_statistics(
        course_id=course_id,
        trimestre_id=trimestre_id
    )
    return jsonify({"statistics": stats}), 200