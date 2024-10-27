from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import config
from .utils.init_curse import init_courses
from .utils.init_roles import init_roles
from .utils.init_Objetivos import init_objectives
from .utils.init_formulas import init_formulas
from .utils.init_status import init_status
from .utils.init_trimestre import init_trimesters_and_periods

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}}, supports_credentials=True)
    

    with app.app_context():
        from app.models.user import User, Permission, UserRole, Role, Teacher, CoordinatorTeacherAssignment
        from app.models.Indicadores import Indicator, IndicatorState, Evaluation, Formula, StudentStatus
        from app.models.peridos import Trimester, Period, Document
        from app.models.ObjAcademico import AcademicObjective, SGCObjective
        from app.models.coures import Course, Nivel
        
        from .routes.auth_routes import auth_bp
        from app.controllers.teacher_controller import teacher_bp
        from app.controllers.user_controller import user_bp
        from app.controllers.courses_controller import courses_bp
        from app.controllers.obj_controller import objective_bp
        from app.controllers.indicator_controller import indicator_bp
        from app.controllers.document_controller import documents_bp
        from app.controllers.compliance_controller import compliance_bp
        from app.controllers.efectivizar_controller import student_status_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(teacher_bp, url_prefix='/api')
        app.register_blueprint(user_bp, url_prefix='/api')
        app.register_blueprint(courses_bp, url_prefix = '/api')
        app.register_blueprint(objective_bp, url_prefix = '/api')
        app.register_blueprint(indicator_bp, url_prefix = '/api')
        app.register_blueprint(documents_bp, url_prefix='/api')
        app.register_blueprint(compliance_bp, url_prefix='/api')
        app.register_blueprint(student_status_bp, url_prefix='/api')
                
        db.create_all()
        init_roles(app)
        init_courses(app)
        init_objectives(app)
        init_formulas(app)
        init_status(app)
        init_trimesters_and_periods(app)
        #init_nivel(app)

    return app