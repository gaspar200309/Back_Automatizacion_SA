def init_asignatura(app):
    with app.app_context():
        from app.models.user import Asignatura
        from app import db 

        asignatur = ['Lenguaje y Literatura ', 'Inglés', 'Quechua', 'Matemática', 'Física', 'Química', 'Biología', 'Ciencias Sociales', 'Dibujo',
                     'Carpintería', 'Música', 'Educación Física', 'Psicología / Filosofía', 'Filosofía', 'Religión', 'Computación'
                     ]
        for name in asignatur:
            asignaturaO = Asignatura.query.filter_by(name_asignatura=name).first()  
            if not asignaturaO:
                new_asignatura = Asignatura(name_asignatura=name)
                db.session.add(new_asignatura)
        db.session.commit()
