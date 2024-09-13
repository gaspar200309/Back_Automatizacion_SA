def init_objectives(app):
    with app.app_context():
        from app.models.ObjAcademico import AcademicObjective, SGCObjective 
        from .. import db
        
        sgc_objectives = [
            {'name': 'GARANTIZAR LA GESTIÓN ACADÉMICA (SGC)', 'description': 'Objetivo orientado a mejorar los resultados en las materias clave.'},
            {'name': 'CONSOLIDAR LOS PROYECTOS PESA+ EN FUNCIONAMIENTO Y GENERAR NUEVOS DE ACUERDO A LOS 5 COMPONENTES DEL PLAN ESTRATÉGICO (SGC).', 'description': 'Objetivo para incentivar la investigación en áreas de interés académico.'},
            {'name': 'OPTIMIZAR EL DESEMPEÑO HOLÍSTICO DEL DOCENTE (SGC).', 'description': 'Objetivo orientado a mejorar los resultados en las materias clave.'},
            {'name': 'AFIANZAR LA FORMACIÓN INTEGRAL DE LOS ESTUDIANTES (SGC)', 'description': 'Objetivo orientado a mejorar los resultados en las materias clave.'}
        ]
        
        academic_objectives = [
            {'name': 'EFECTIVIZAR LOS PROCEDIMIENTOS ACADÉMICO ADMINISTRATIVOS EXTERNOS E INTERNOS', 'description': 'Asegurar que los estándares de calidad en la enseñanza se cumplan.'},
            {'name': 'MEJORAR EL SISTEMA INFORMÁTICO DE GESTIÓN ACADÉMICA, RESPECTO AL MANEJO DE LA INFORMACIÓN.', 'description': 'Reducir los tiempos y mejorar la eficiencia en los procesos administrativos.'},
            {'name': 'OPTIMIZAR LA ESTRATEGIA COMUNICACIONAL DEL ÁREA ACADÉMICA HACIA EL MEDIO INTERNO Y EXTERNO DEL COLEGIO', 'description': 'Asegurar que los estándares de calidad en la enseñanza se cumplan.'},
            {'name': 'DESARROLLAR UN SISTEMA DE FORMACIÓN HÍBRIDA (PRESENCIAL/A DISTANCIA – SINCRÓNICO/ASÍNCRONO)', 'description': 'Reducir los tiempos y mejorar la eficiencia en los procesos administrativos.'},
            {'name': 'REESTRUCTURAR EL SISTEMA DE GESTIÓN DE CALIDAD, EN EL ÁMBITO ACADÉMICO, DE ACUERDO A LA NUEVA VISIÓN DEL COLEGIO', 'description': 'Asegurar que los estándares de calidad en la enseñanza se cumplan.'},
            {'name': 'ESTABLECER EL PROYECTO EDITORIAL PARA LA GENERACIÓN DE RECURSOS EDUCATIVOS CURRICULARES Y OTROS COMPLEMENTARIOS', 'description': 'Reducir los tiempos y mejorar la eficiencia en los procesos administrativos.'},
            {'name': 'IMPLEMENTAR EL PROYECTO DE INGLÉS COMMUNICATION (DUOLINGO Y COMPONENTE SPEAKING)', 'description': 'Asegurar que los estándares de calidad en la enseñanza se cumplan.'},
            {'name': 'FORTALECER EL PROYECTO SUPÉRATE PARA LA OPTIMIZACIÓN DE LA PARTICIPACIÓN INSTITUCIONAL EN COMPETENCIAS', 'description': 'Reducir los tiempos y mejorar la eficiencia en los procesos administrativos.'},
            {'name': 'CONSOLIDAR EL SISTEMA HOLÍSTICO DE EVALUACIÓN CONTINUA DOCENTE', 'description': 'Asegurar que los estándares de calidad en la enseñanza se cumplan.'},
            {'name': 'GENERAR ESTADÍSTICAS BÁSICAS RELACIONADAS A LA FORMACIÓN DEL GRUPO ESTUDIANTIL PARA LA TOMA DE DECISIONES.', 'description': 'Reducir los tiempos y mejorar la eficiencia en los procesos administrativos.'},
            {'name': 'IMPLEMENTAR EL MÉTODO PAES EN LOS DIFERENTES ÁMBITOS DEL PROCESO ENSEÑANZA Y APRENDIZAJE EN TODOS LOS CURSOS', 'description': 'Asegurar que los estándares de calidad en la enseñanza se cumplan.'},
            {'name': 'AFIANZAR LOS PROCESOS DE APOYO COMPLEMENTARIO DOCENTE-ESTUDIANTE Y ESTUDANTE-ESTUDIANTE EN EL MARCO DEL PRINCIPIO DE VIDA EN COMUNIDAD', 'description': 'Reducir los tiempos y mejorar la eficiencia en los procesos administrativos.'},
            {'name': 'DISMINUIR LOS ÍNDICES DE FACTORES ACTITUDINALES NEGATIVOS Y/O DE RIESGO EN LOS ESTUDIANTES.', 'description': 'Asegurar que los estándares de calidad en la enseñanza se cumplan.'},
            {'name': 'CONSOLIDAR EL PROCESO DE ADMISIÓN PARA ASEGURAR EL INGRESO DE PERFILES ESTUDIANTILES ACORDES A LOS REQUERIMIENTOS DEL COLEGIO.', 'description': 'Reducir los tiempos y mejorar la eficiencia en los procesos administrativos.'},
        ]
        
        for objective_data in academic_objectives:
            objective = AcademicObjective.query.filter_by(name=objective_data['name']).first()
            if not objective:
                new_objective = AcademicObjective(name=objective_data['name'], description=objective_data['description'])
                db.session.add(new_objective)

        for objective_data in sgc_objectives:
            objective = SGCObjective.query.filter_by(name=objective_data['name']).first()
            if not objective:
                new_objective = SGCObjective(name=objective_data['name'], description=objective_data['description'])
                db.session.add(new_objective)

        db.session.commit()
