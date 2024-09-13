from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
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
    academic_objective_id = Column(Integer, ForeignKey('academic_objectives.id'))
    sgc_objective_id = Column(Integer, ForeignKey('sgc_objectives.id'))
    evaluations = relationship('Evaluation', back_populates='indicator')
    users = relationship('User', secondary=user_indicator, back_populates='indicators')

    academic_objective = relationship('AcademicObjective', back_populates='indicators')
    sgc_objective = relationship('SGCObjective', back_populates='indicators')
    formula_id = db.Column(db.Integer, db.ForeignKey('formulas.id'))
    formula = db.relationship('Formula', back_populates='indicators')
    



class IndicatorState(db.Model):
    __tablename__ = 'indicator_states'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey('indicators.id'))
    indicator = relationship('Indicator', back_populates='evaluations')
    

