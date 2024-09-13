from sqlalchemy.exc import SQLAlchemyError
from app.models.coures import Nivel, Course
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

git remote remove https://github.com/gaspar200309/C-San-Agustin-Automatizacion.git