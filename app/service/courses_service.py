from sqlalchemy.exc import SQLAlchemyError
from app.models.coures import Nivel, Course
from app.models.user import Teacher
from app import db

def get_all_courses():
    try:
        courses = db.session.query(Course).join(Nivel).all()
        return [{
            "course_id":course.id,
            "course_name": course.name,
            "paralelo": course.paralelo,
            "nivel": course.nivel.name
        } for course in courses]
    except SQLAlchemyError as e:
        db.session.rollback()  
        print(f"Error: {e}")
        return []

def get_courses_by_teacher_id(teacher_id):
    try:
        teacher = db.session.query(Teacher).filter_by(id=teacher_id).first()
        if not teacher:
            return None, "Teacher not found"
        
        # Retrieve courses associated with the teacher
        courses = teacher.courses  # SQLAlchemy relationship is already defined on Teacher model
        
        return courses, None
    except Exception as e:
        return None, str(e)