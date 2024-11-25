from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .. import db

teacher_course = Table('teacher_course', db.Model.metadata,
    Column('teacher_id', Integer, ForeignKey('teacher.id', ondelete='CASCADE'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True)
)

class Nivel(db.Model):
    __tablename__ = 'niveles'  
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    courses = relationship('Course', back_populates='nivel')  


class Course(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    paralelo = Column(String(50), nullable= False)
    name_paralelo = Column(String(50), nullable = False)
    nivel_id = Column(Integer, ForeignKey('niveles.id'), nullable=False)
    nivel = relationship('Nivel', back_populates='courses')
    reports = relationship('Report', back_populates='course')
    teachers = relationship('Teacher', secondary=teacher_course, back_populates='courses')
