from app.models.Indicadores import Indicator
from app import db

def create_indicator(data):
    try:
        indicator = Indicator(
            name=data.get('name'),
            delivery_deadline=data.get('delivery_deadline'),
            due_date=data.get('due_date'),
            improvement_action=data.get('improvement_action'),
            expected_result=data.get('expected_result'),
            academic_objective_id=data.get('academic_objective_id'),
            sgc_objective_id=data.get('sgc_objective_id'),
            formula_id=data.get('formula_id')
        )
        db.session.add(indicator)
        db.session.commit()
        return indicator
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creating indicator: {str(e)}")

def get_all_indicators():
    try:
        indicators = db.session.query(Indicator).all()
        return indicators
    except Exception as e:
        raise Exception(f"Error retrieving indicators: {str(e)}")