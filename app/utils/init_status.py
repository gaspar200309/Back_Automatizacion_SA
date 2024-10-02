
def init_status(app):
    from app.models.Indicadores import IndicatorState  
    from .. import db

    with app.app_context():
        states = ['Sí', 'No', 'Retraso', 'Incompleto', 'No corresponde'] 
        
        for state_name in states:
            state = IndicatorState.query.filter_by(name=state_name).first()
            if not state:
                new_state = IndicatorState(name=state_name)
                db.session.add(new_state)
        
        db.session.commit()
