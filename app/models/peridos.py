from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from .. import db

class Trimester(db.Model):
    __tablename__ = 'trimesters'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

class Period(db.Model):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)  
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    indicators = relationship('Indicator', back_populates='period')


class Document(db.Model):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    delivered = Column(Boolean, default=False)
    upload_date = Column(Date, nullable=False)  
    indicator_id = Column(Integer, ForeignKey('indicators.id'))  
    period_id = Column(Integer, ForeignKey('periods.id')) 

    indicator = relationship('Indicator', back_populates='documents')
