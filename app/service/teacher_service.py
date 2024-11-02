from app import db
from app.models.coures import Course
from app.models.user import Teacher, User, CoordinatorTeacherAssignment

def register_teacher(name, last_name, asignatura, course_ids):
    # Crear un nuevo profesor
    new_teacher = Teacher(
        name=name,
        last_name=last_name,
        asignatura=asignatura
    )
    
    # Añadir el profesor a la sesión antes de asociarle los cursos
    db.session.add(new_teacher)
    
    # Asignar cursos al profesor
    for course_id in course_ids:
        course = db.session.query(Course).filter_by(id=course_id).first()
        if course is None:
            raise ValueError(f"El curso con id {course_id} no existe")
        new_teacher.courses.append(course)
    
    # Guardar cambios en la base de datos
    db.session.commit()

    return new_teacher



def assign_teacher_to_coordinator(teacher_id, coordinator_id):
    teacher = Teacher.query.get(teacher_id)
    coordinator = User.query.get(coordinator_id)
    if not teacher or not coordinator:
        return None
    assignment = CoordinatorTeacherAssignment(teacher_id=teacher.id, coordinator_id=coordinator.id)
    db.session.add(assignment)
    db.session.commit()
    return assignment

def get_all_teachers():
    teachers = db.session.query(Teacher).all()
    
    teacher_list = []
    for teacher in teachers:
        teacher_data = {
            'id': teacher.id,
            'name': teacher.name,
            'last_name': teacher.last_name,
            'asignatura': teacher.asignatura,
            'courses': [{
                'course_id': course.id,
                'course_name': course.name,
                'nivel': course.nivel.name  # Relación con nivel
            } for course in teacher.courses]  # Obtener todos los cursos asociados al profesor
        }
        teacher_list.append(teacher_data)
    return teacher_list

def get_teacher_by_id(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return None
    
    teacher_data = {
        'id': teacher.id,
        'name': teacher.name,
        'last_name': teacher.last_name,
        'asignatura': teacher.asignatura,
        'courses': [{
            'course_id': course.id,
            'course_name': course.name,
            'nivel': course.nivel.name  
        } for course in teacher.courses] 
    }
    
    return teacher_data
    

def update_teacher(teacher_id, name, last_name, asignatura, course_ids):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError("Profesor no encontrado")
    
    teacher.name = name
    teacher.last_name = last_name
    teacher.asignatura = asignatura
    
    if not isinstance(course_ids, list):
        course_ids = [course_ids]
    
    teacher.courses = []  
    for course_id in course_ids:
        course = Course.query.get(course_id)
        if not course:
            raise ValueError(f"Curso con ID {course_id} no encontrado")
        teacher.courses.append(course)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al actualizar profesor: {str(e)}")
    
    return teacher


def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError("Profesor no encontrado")
    
    db.session.delete(teacher)
    db.session.commit()
    
def get_teacher_count():
    return Teacher.query.count()