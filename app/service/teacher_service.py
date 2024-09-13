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
