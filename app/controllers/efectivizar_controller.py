from flask import Blueprint, request, jsonify
from app.service.efectivizar_service import StudentStatusService

student_status_bp = Blueprint('student_status_bp', __name__)

@student_status_bp.route('/student-status', methods=['POST'])
def create_or_update_student_status():
    data = request.get_json()

    # Obtener datos del cuerpo de la solicitud
    indicator_id = data.get('indicator_id')
    active_students = data.get('active_students')
    inactive_students = data.get('inactive_students')

    if not indicator_id or active_students is None or inactive_students is None:
        return jsonify({"message": "Faltan datos necesarios"}), 400

    # Llamar al servicio para crear o actualizar el estado de los estudiantes
    student_status = StudentStatusService.create_or_update_student_status(
        indicator_id=indicator_id,
        active_students=active_students,
        inactive_students=inactive_students
    )

    return jsonify({
        "message": "Estado de estudiantes registrado/actualizado exitosamente",
        "indicator_id": student_status.indicator_id,
        "active_students": student_status.active_students,
        "inactive_students": student_status.inactive_students
    }), 200

# Ruta para obtener el estado de los estudiantes por indicador
@student_status_bp.route('/student-status/<int:indicator_id>', methods=['GET'])
def get_student_status(indicator_id):
    student_status = StudentStatusService.get_student_status(indicator_id)

    if not student_status:
        return jsonify({"message": "No se encontró el estado de estudiantes para este indicador"}), 404

    return jsonify({
        "indicator_id": student_status.indicator_id,
        "active_students": student_status.active_students,
        "inactive_students": student_status.inactive_students
    }), 200


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