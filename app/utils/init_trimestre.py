def init_trimesters_and_periods(app):
    with app.app_context():
        from .. import db
        from app.models.peridos import Trimester, Period 
        
        trimesters = [
            {'name': 'Primer Trimestre', 'start_date': '2025-01-01', 'end_date': '2025-04-30'},
            {'name': 'Segundo Trimestre', 'start_date': '2025-05-01', 'end_date': '2025-07-31'},
            {'name': 'Tercer Trimestre', 'start_date': '2025-08-01', 'end_date': '2025-10-31'},
            {'name': 'Cuarto Trimestre', 'start_date': '2025-11-01', 'end_date': '2025-12-31'}
        ]
        
        for t_data in trimesters:
            trimester = Trimester.query.filter_by(name=t_data['name']).first()
            if not trimester:
                new_trimester = Trimester(name=t_data['name'], start_date=t_data['start_date'], end_date=t_data['end_date'])
                db.session.add(new_trimester)
        
        periods = [
            # Primer Trimestre
            {'name': 'Enero 2025', 'start_date': '2025-01-01', 'end_date': '2025-01-31', 'trimester_name': 'Primer Trimestre'},
            {'name': 'Febrero 2025', 'start_date': '2025-02-01', 'end_date': '2025-02-28', 'trimester_name': 'Primer Trimestre'},
            {'name': 'Marzo 2025', 'start_date': '2025-03-01', 'end_date': '2025-03-31', 'trimester_name': 'Primer Trimestre'},
            {'name': 'Abril 2025', 'start_date': '2025-04-01', 'end_date': '2025-04-30', 'trimester_name': 'Primer Trimestre'},

            # Segundo Trimestre
            {'name': 'Mayo 2025', 'start_date': '2025-05-01', 'end_date': '2025-05-31', 'trimester_name': 'Segundo Trimestre'},
            {'name': 'Junio 2025', 'start_date': '2025-06-01', 'end_date': '2025-06-30', 'trimester_name': 'Segundo Trimestre'},
            {'name': 'Julio 2025', 'start_date': '2025-07-01', 'end_date': '2025-07-31', 'trimester_name': 'Segundo Trimestre'},

            # Tercer Trimestre
            {'name': 'Agosto 2025', 'start_date': '2025-08-01', 'end_date': '2025-08-31', 'trimester_name': 'Tercer Trimestre'},
            {'name': 'Septiembre 2025', 'start_date': '2025-09-01', 'end_date': '2025-09-30', 'trimester_name': 'Tercer Trimestre'},
            {'name': 'Octubre 2025', 'start_date': '2025-10-01', 'end_date': '2025-10-31', 'trimester_name': 'Tercer Trimestre'},

            # Cuarto Trimestre
            {'name': 'Noviembre 2025', 'start_date': '2025-11-01', 'end_date': '2025-11-30', 'trimester_name': 'Cuarto Trimestre'},
            {'name': 'Diciembre 2025', 'start_date': '2025-12-01', 'end_date': '2025-12-31', 'trimester_name': 'Cuarto Trimestre'},
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
