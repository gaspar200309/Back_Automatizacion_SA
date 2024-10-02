from app import db
from app.models.coures import Course
from app.models.user import Teacher, User, CoordinatorTeacherAssignment

def register_teacher(name, last_name, asignatura, course_id):
    # Crear un nuevo profesor
    new_teacher = Teacher(
        name=name,
        last_name=last_name,
        asignatura=asignatura
    )
    
    course = db.session.query(Course).filter_by(id=course_id).first()
    
    if course is None:
        raise ValueError("El curso proporcionado no existe")

    new_teacher.courses.append(course)
    
    db.session.add(new_teacher)
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
    

def update_teacher(teacher_id, name, last_name, asignatura, course_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError("Profesor no encontrado")
    
    teacher.name = name
    teacher.last_name = last_name
    teacher.asignatura = asignatura
    
    # Actualizar el curso
    teacher.courses = []  # Limpiar cursos existentes
    course = Course.query.get(course_id)
    if not course:
        raise ValueError("Curso no encontrado")
    teacher.courses.append(course)
    
    db.session.commit()
    return teacher

def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError("Profesor no encontrado")
    
    db.session.delete(teacher)
    db.session.commit()