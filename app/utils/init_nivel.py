def init_nivel(app):
    with app.app_context():
        from app.models.coures import Level
        from app import db 

        niveles = ['Preparatorio', 'Profundización', 'Expansion']
        for name in niveles:
            nivel = Level.query.filter_by(name=name).first()
            if not nivel:
                new_nivel = Level(name=name)
                db.session.add(new_nivel)
        db.session.commit()
