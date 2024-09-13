def init_courses(app):
    with app.app_context():
        print("Iniciando registro de cursos...")  # Añadir depuración

        from app.models.coures import Course, Nivel
        from .. import db

        courses_data = generate_courses()

        for course_data in courses_data:
            # Buscar o crear el nivel si no existe
            nivel = Nivel.query.filter_by(name=course_data['nivel']).first()

            if not nivel:
                nivel = Nivel(name=course_data['nivel'])
                db.session.add(nivel)
                db.session.commit()  # Guardar el nuevo nivel en la base de datos
            

            # Buscar o crear el curso si no existe
            course = Course.query.filter_by(name=course_data['name'], nivel=nivel).first()

            if not course:
                new_course = Course(
                    name=course_data['name'],
                    paralelo=course_data['paralelo'],
                    name_paralelo=course_data['name_paralelo'],
                    nivel=nivel
                )
                db.session.add(new_course)
           

        db.session.commit()
        print("Registro de cursos completado")



def generate_courses():
    courses_data = []
    
    # Generar cursos para 'Primaria'
    niveles_primaria = ['Primaria']
    grados_primaria = ['Sexto']
    paralelos = ['A', 'B', 'C', 'D']

    for nivel in niveles_primaria:
        for grado in grados_primaria:
            for paralelo in paralelos:
                name = f"{grado} {paralelo}"
                name_paralelo = f"{grado[0]}P{paralelo}"
                courses_data.append({
                    'name': name,
                    'paralelo': paralelo,
                    'name_paralelo': name_paralelo,
                    'nivel': nivel
                })

    # Generar cursos para 'Secundaria' (de Primero a Sexto)
    niveles_secundaria = ['Secundaria']
    grados_secundaria = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto']

    for nivel in niveles_secundaria:
        for grado in grados_secundaria:
            for paralelo in paralelos:
                name = f"{grado} {paralelo}"
                name_paralelo = f"{grado[0]}S{paralelo}"
                courses_data.append({
                    'name': name,
                    'paralelo': paralelo,
                    'name_paralelo': name_paralelo,
                    'nivel': nivel
                })

    return courses_data
