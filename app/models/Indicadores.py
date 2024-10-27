from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import user_indicator
from .. import db

class Formula(db.Model):
    __tablename__ = 'formulas'
    id = Column(Integer, primary_key=True)
    formula = Column(String(250), nullable=False)
    
    indicators = db.relationship('Indicator', back_populates='formula',
                                 foreign_keys='Indicator.formula_id')
    
class Indicator(db.Model):
    __tablename__ = 'indicators'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    delivery_deadline = Column(Date, nullable=True) #  fecha límite de entrega
    due_date = Column(Date, nullable=False)  #Fecha de vencimiento¿
    improvement_action = Column(String(250)) # Mejora accion
    expected_result = Column(String(50), nullable=False) # resultado esperado
    is_completed = Column(Boolean, default=False)
    academic_objective_id = Column(Integer, ForeignKey('academic_objectives.id'))
    formula_id = db.Column(db.Integer, db.ForeignKey('formulas.id'), nullable=False)
    sgc_objective_id = Column(Integer, ForeignKey('sgc_objectives.id'))
    evaluations = relationship('Evaluation', back_populates='indicator', cascade='all, delete-orphan')
    users = relationship('User', secondary=user_indicator, back_populates='indicators')
    period_id = Column(Integer, ForeignKey('periods.id')) 

    academic_objective = relationship('AcademicObjective', back_populates='indicators')
    sgc_objective = relationship('SGCObjective', back_populates='indicators')
    formula = relationship('Formula', back_populates='indicators')
    evaluations = relationship('Evaluation', back_populates='indicator', cascade='all, delete-orphan')
    users = relationship('User', secondary=user_indicator, back_populates='indicators')
    documents = relationship('Document', back_populates='indicator')
    period = relationship('Period', back_populates='indicators')
    reports = relationship('Report', back_populates='indicator')
    student_status = relationship('StudentStatus', back_populates='indicator', uselist=False)


class IndicatorState(db.Model):
    __tablename__ = 'indicator_states'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    porcentage = Column(Integer, nullable = True)
    indicator_id = Column(Integer, ForeignKey('indicators.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable = True)  
    state_id = Column(Integer, ForeignKey('indicator_states.id'), nullable = True)
    period_id = Column(Integer, ForeignKey('periods.id'), nullable=True) 
    trimestre_id = Column(Integer, ForeignKey('trimesters.id'), nullable  = True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True) 
    parallel = Column(String(10), nullable=True)      
    
    indicator = relationship('Indicator', back_populates='evaluations')
    teacher = relationship('Teacher') 
    state = relationship('IndicatorState')  
    period = relationship('Period')  
    trimestre = relationship('Trimester') 
    course = relationship('Course')  
     
    
class StudentStatus(db.Model):
    __tablename__ = 'student_status'
    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey('indicators.id'), nullable=False)
    active_students = Column(Integer, default=0, nullable=False)
    inactive_students  = Column(Integer, default=0, nullable=False)
    registered_at = Column(DateTime, default=func.now()) 

    indicator = relationship('Indicator', back_populates='student_status')

class Report(db.Model):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True)
    asistencia = Column(Integer)
    licencia = Column(Integer)
    incidencias = Column(Integer)
    communication = Column(Integer)
    indicator_id = Column(Integer, ForeignKey('indicators.id'), nullable=False)
    trimestre_id = Column(Integer, ForeignKey('trimesters.id'), nullable=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable = True) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable = True)

    indicator = relationship('Indicator', back_populates='reports')
    trimestre = relationship('Trimester', back_populates='reports')
    course = relationship('Course', back_populates='reports')
    teacher = relationship('Teacher', back_populates='reports')
    user = relationship('User', back_populates='reports')


