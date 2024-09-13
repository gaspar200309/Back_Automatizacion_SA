from flask import Blueprint, request, jsonify
from app.service.teacher_service import register_teacher, assign_teacher_to_coordinator, get_all_teachers

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/teachers', methods=['POST'])
def create_teacher():
    data = request.get_json()
    
    name = data.get('firstName')
    last_name = data.get('lastName')
    asignatura = data.get('subjects')
    course_id = data.get('course')  

    if not name or not last_name or not asignatura or not course_id:
        return jsonify({'error': 'Faltan datos necesarios para registrar el profesor'}), 400
    
    try:
        new_teacher = register_teacher(name, last_name, asignatura, course_id)
        
        return jsonify({
            'message': 'Profesor registrado exitosamente',
            'teacher': {
                'id': new_teacher.id,
                'name': new_teacher.name,
                'last_name': new_teacher.last_name,
                'asignatura': new_teacher.asignatura,
                'course_id': course_id
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error al registrar el profesor'}), 500


@teacher_bp.route('/teachers/<int:teacher_id>/assign', methods=['POST'])
def assign_teacher(teacher_id):
    data = request.get_json()
    coordinator_id = data.get('coordinator_id')
    if not coordinator_id:
        return jsonify({"error": "Coordinator ID is required"}), 400
    
    assignment = assign_teacher_to_coordinator(teacher_id, coordinator_id)
    if not assignment:
        return jsonify({"error": "Invalid Teacher or Coordinator ID"}), 404
    
    return jsonify({"message": "Teacher assigned successfully"}), 200

@teacher_bp.route('/teachers', methods=['GET'])
def list_teachers():
    try:
        teachers = get_all_teachers()
        
        return jsonify(teachers), 200
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error al obtener los profesores'}), 500
