from flask import jsonify
from app.models.user import Teacher, User
from app.models.Indicadores import Indicator
from sqlalchemy import func
from app import db

class SummaryService:
    @staticmethod
    def get_summary_counts():
        teacher_count = Teacher.query.count()
        user_count = User.query.count()
        
        total_indicators = db.session.query(func.count(Indicator.id)).scalar()
        completed_indicators = db.session.query(func.count(Indicator.id)).filter(Indicator.is_completed == True).scalar()
        incomplete_indicators = total_indicators - completed_indicators
        
        return {
            'total_teachers': teacher_count,
            'total_users': user_count,
            'indicators': {
                'total': total_indicators,
                'completed': completed_indicators,
                'incomplete': incomplete_indicators
            }
        }
