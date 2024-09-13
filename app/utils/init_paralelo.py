def init_paralelo(app):
    with app.app_context():
        from app.models.coures import Parallel
        from app import db 

        paralelos = ['A', 'B', 'C', 'D']
        for name in paralelos:
            paralelo = Parallel.query.filter_by(name=name).first()
            if not paralelo:
                new_paralelo = Parallel(name=name)
                db.session.add(new_paralelo)
        db.session.commit()
