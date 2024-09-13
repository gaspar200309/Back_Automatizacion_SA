from sqlalchemy import Column, Integer, String, Boolean
from .. import db

class Trimester(db.Model):
    __tablename__ = 'trimesters'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

class Period(db.Model):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

class Document(db.Model):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(250), nullable=False)
    is_delivered = Column(Boolean, default=False)
