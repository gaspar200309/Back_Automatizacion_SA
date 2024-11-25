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
