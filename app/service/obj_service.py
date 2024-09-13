from app.models.ObjAcademico import AcademicObjective, SGCObjective
from app import db

def get_academic_objectives():
    return db.session.query(AcademicObjective.id, AcademicObjective.name).all()

def get_sgc_objectives():
    return db.session.query(SGCObjective.id, SGCObjective.name).all()

