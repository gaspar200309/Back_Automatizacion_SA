from flask import Blueprint, request, jsonify
from app.service.teacher_service import register_teacher, assign_teacher_to_coordinator, get_all_teachers, get_teacher_by_id, update_teacher, delete_teacher

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/teachers', methods=['POST'])
def create_teacher():
    data = request.get_json()
    print(data)
    name = data.get('firstName')
    last_name = data.get('lastName')
    asignatura = data.get('subjects')
    course_id = data.get('course_ids')  

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
    
#Get teacher for id a controller
@teacher_bp.route('/teachers/<int:teacher_id>', methods = ['GET'])
def get_teacherb(teacher_id):
    try:
        teacher = get_teacher_by_id(teacher_id)
        
        return jsonify(teacher), 200
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error al obtener el profesor'}), 500
    

# ... (otras rutas existentes)

@teacher_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher_route(teacher_id):
    data = request.get_json()
    
    required_fields = {'firstName': 'nombre', 'lastName': 'apellido', 
                      'subjects': 'asignatura', 'course_ids': 'cursos'}
    missing_fields = [required_fields[field] for field in required_fields 
                     if not data.get(field)]
    
    if missing_fields:
        return jsonify({
            'error': f'Faltan datos necesarios: {", ".join(missing_fields)}'
        }), 400
    
    try:
        updated_teacher = update_teacher(
            teacher_id=teacher_id,
            name=data['firstName'],
            last_name=data['lastName'],
            asignatura=data['subjects'],
            course_ids=data['course_ids']
        )
        
        return jsonify({
            'message': 'Profesor actualizado exitosamente',
            'teacher': {
                'id': updated_teacher.id,
                'name': updated_teacher.name,
                'last_name': updated_teacher.last_name,
                'asignatura': updated_teacher.asignatura,
                'courses': [{
                    'course_id': course.id,
                    'course_name': course.name,
                    'nivel': course.nivel.name
                } for course in updated_teacher.courses]
            }
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Error al actualizar profesor: {str(e)}'}), 500

@teacher_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher_route(teacher_id):
    try:
        delete_teacher(teacher_id)
        return jsonify({'message': 'Profesor eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error al eliminar el profesor'}), 500

    
 