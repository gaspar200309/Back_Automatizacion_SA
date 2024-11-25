def init_formulas(app):
    with app.app_context():
        from app.models.Indicadores import Formula
        from .. import db

        formulas = ['Sin formula',
                    '(5) ÓPTIMO, (4) MUY BUENO, (3) BUENO, (2) REGULAR, (1) INSUFICIENTE',
                    'Tasa=(Nro. de PGO recibidos)/(Nro. total de la población)',
                    'Tasa=(Nro. de planes curriculares - contenido publicados en plataforma)/(Nro. total de la población)',
                    'Tasa=(Nro. de docentes que cumplieron la entrega de notas cada periodo)/(Nro. total de la población docente)',
                    'USAR MEDIA - PROMEDIO, REUNIRSE CON BERNARDO',
                    ] 

        for formula_name in formulas:
            formula = Formula.query.filter_by(formula=formula_name).first()  
            if not formula:
                new_formula = Formula(formula=formula_name)
                db.session.add(new_formula)

        db.session.commit()
