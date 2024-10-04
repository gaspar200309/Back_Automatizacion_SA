def init_trimesters_and_periods(app):
    with app.app_context():
        from .. import db
        from app.models.peridos import Trimester, Period 
        
        trimesters = [
            {'name': 'Primer Trimestre', 'start_date': '2024-01-01', 'end_date': '2024-04-01'},
            {'name': 'Segundo Trimestre', 'start_date': '2024-04-02', 'end_date': '2024-07-01'},
            {'name': 'Tercer Trimestre', 'start_date': '2024-07-02', 'end_date': '2024-10-01'}
        ]
        
        for t_data in trimesters:
            trimester = Trimester.query.filter_by(name=t_data['name']).first()
            if not trimester:
                new_trimester = Trimester(name=t_data['name'], start_date=t_data['start_date'], end_date=t_data['end_date'])
                db.session.add(new_trimester)
        
        periods = [
            {'name': 'Enero-Febrero 2024', 'start_date': '2024-01-01', 'end_date': '2024-02-28', 'trimester_name': 'Primer Trimestre'},
            {'name': 'Marzo-Abril 2024', 'start_date': '2024-03-01', 'end_date': '2024-04-01', 'trimester_name': 'Primer Trimestre'},
            
            {'name': 'Mayo-Junio 2024', 'start_date': '2024-05-01', 'end_date': '2024-06-30', 'trimester_name': 'Segundo Trimestre'},
            {'name': 'Julio-Agosto 2024', 'start_date': '2024-07-01', 'end_date': '2024-08-31', 'trimester_name': 'Segundo Trimestre'},
            
            {'name': 'Septiembre-Octubre 2024', 'start_date': '2024-09-01', 'end_date': '2024-10-31', 'trimester_name': 'Tercer Trimestre'},
            {'name': 'Noviembre-Diciembre 2024', 'start_date': '2024-11-01', 'end_date': '2024-12-31', 'trimester_name': 'Tercer Trimestre'}
        ]
        
        for p_data in periods:
            period = Period.query.filter_by(name=p_data['name']).first()
            if not period:
                trimester = Trimester.query.filter_by(name=p_data['trimester_name']).first()
                if trimester:
                    new_period = Period(
                        name=p_data['name'], 
                        start_date=p_data['start_date'], 
                        end_date=p_data['end_date'], 
                        trimester_id=trimester.id 
                    )
                    db.session.add(new_period)
        
        db.session.commit()
