from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from .coures import teacher_course
from sqlalchemy.orm import relationship
from .. import db


user_indicator = Table('user_indicator', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('indicator_id', Integer, ForeignKey('indicators.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))  
    photo = Column(String(255), nullable=True)  
    password_hash = Column(String(512), nullable=False)
    
    roles = relationship('UserRole', back_populates='user')
    coordinator_assignments = relationship('CoordinatorTeacherAssignment', back_populates='coordinator')
    indicators = relationship('Indicator', secondary=user_indicator, back_populates='users')
    reports = relationship('Report', back_populates='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




role_permission = Table('role_permission', db.Model.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='roles')
    role = relationship('Role', back_populates='users')


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    permissions = relationship('Permission', secondary=role_permission, back_populates='roles')
    users = relationship('UserRole', back_populates='role')

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    roles = relationship('Role', secondary=role_permission, back_populates='permissions')


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    asignatura = Column(String(50), nullable=False)
    
    assignments = relationship('CoordinatorTeacherAssignment', back_populates='teacher')
    evaluations = relationship('Evaluation', back_populates='teacher')
    reports = relationship('Report', back_populates='teacher')
    courses = relationship('Course', secondary=teacher_course, back_populates='teachers')



class CoordinatorTeacherAssignment(db.Model):
    __tablename__ = 'coordinator_teacher_assignments'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id', ondelete='CASCADE'))  
    coordinator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', back_populates='assignments')
    coordinator = relationship('User', back_populates='coordinator_assignments')