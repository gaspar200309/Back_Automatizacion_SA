from app import db
from app.models.Indicadores import StudentStatus, Report, IndicatorState, Evaluation
from app.models.coures import Course
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

class StudentStatusService:

    @staticmethod
    def create_or_update_student_status(indicator_id, active_students, inactive_students):
        student_status = StudentStatus.query.filter_by(indicator_id=indicator_id).first()

        if not student_status:
            student_status = StudentStatus(
                indicator_id=indicator_id,
                active_students=active_students,
                inactive_students=inactive_students
            )
            db.session.add(student_status)
        else:
            # Si ya existe, actualizar los valores
            student_status.active_students = active_students
            student_status.inactive_students = inactive_students
        
        # Guardar los cambios
        db.session.commit()
        return student_status

    @staticmethod
    def get_student_status(indicator_id):
        # Buscar el estado de estudiantes para un indicador específico
        return StudentStatus.query.filter_by(indicator_id=indicator_id).first()
    
    @staticmethod
    def register_licenses(indicator_id, trimestre_id, course_id, licencia):
        try:
            report = Report(
                indicator_id=indicator_id,
                trimestre_id=trimestre_id,
                course_id=course_id,
                licencia=licencia,
            )
            db.session.add(report)
            db.session.commit()
            
            report_dict = {
                "id": report.id,
                "indicator_id": report.indicator_id,
                "trimestre_id": report.trimestre_id,
                "course_id": report.course_id,
                "licencia": report.licencia,
            }
            
            return {"message": "Report registered successfully", "report": report_dict}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        
    @staticmethod
    def get_detailed_statistics():
        statistics = {
            "courses": [],
            "general": {}
        }

        total_estudiantes_estatico = 1060  

        # Filtra los datos con indicator_id = 12 e incluye el nombre del curso en la consulta
        courses_data = db.session.query(
            Report.course_id,
            Course.name.label("course_name"),  # Obtén el nombre del curso
            Report.trimestre_id,
            func.sum(Report.licencia).label("total_licencias")
        ).join(Course, Course.id == Report.course_id).filter(Report.indicator_id == 12).group_by(Report.course_id, Report.trimestre_id, Course.name).all()

        course_dict = {}
        for data in courses_data:
            course_id = data.course_id
            course_name = data.course_name  # Almacena el nombre del curso
            total_licencias = data.total_licencias or 0

            # Calcula el porcentaje basado en el valor estático
            porcentaje_licencias = (total_licencias / total_estudiantes_estatico) * 100 if total_estudiantes_estatico else 0

            # Estructura para cada trimestre, asegurando que el porcentaje no exceda el 100%
            trimester_data = {
                "total_licencias": total_licencias,
                "porcentaje_licencias": min(porcentaje_licencias, 100)
            }

            if course_id not in course_dict:
                course_dict[course_id] = {
                    "course_id": course_id,
                    "course_name": course_name,
                    "trimesters": {}
                }
            
            # Agrega el trimestre al diccionario `trimesters` de cada curso, usando el trimestre_id como clave
            course_dict[course_id]["trimesters"][str(data.trimestre_id)] = trimester_data

        # Convierte el diccionario en una lista de cursos para el JSON final
        statistics["courses"] = list(course_dict.values())

        # Estadísticas generales para indicator_id = 12
        result_general = db.session.query(
            func.sum(Report.licencia).label("total_licencias")
        ).filter(Report.indicator_id == 12).first()

        if result_general:
            total_licencias_general = result_general.total_licencias or 0
            indice_general = (total_licencias_general / total_estudiantes_estatico) * 100 if total_estudiantes_estatico else 0
            statistics["general"] = {
                "total_licencias": total_licencias_general,
                "indice": min(indice_general, 100)  # Limitar a un máximo de 100%
            }
        else:
            statistics["general"] = {
                "total_licencias": 0,
                "indice": 0
            }

        return statistics

    @staticmethod
    def register_incidences(data):
        indicator_id = data.get("indicator_id")
        trimestre_id = data.get("trimestre_id")
        course_id = data.get("course_id")
        incidencias = data.get("incidencias", 0)

        report = Report.query.filter_by(
            indicator_id=indicator_id,
            trimestre_id=trimestre_id,
            course_id=course_id
        ).first()

        if report:
            # Si ya existe, actualiza la cantidad de incidencias
            report.incidencias = incidencias
        else:
            # Si no existe, crea un nuevo reporte
            report = Report(
                indicator_id=indicator_id,
                trimestre_id=trimestre_id,
                course_id=course_id,
                incidencias=incidencias
            )
            db.session.add(report)

        db.session.commit()
        return {"message": "Incidencia registrada con éxito."}



    @staticmethod
    def get_incidences_statistics(course_id=None, trimester_id=None, semester_id=None):
        TOTAL_ESTUDIANTES_STATIC = 1060

        query = db.session.query(
            Report.course_id,
            Course.name.label("course_name"),
            Report.trimestre_id,
            func.sum(Report.incidencias).label("total_incidencias")
        ).join(Course, Course.id == Report.course_id) \
        .filter(Report.indicator_id == 13)

        if course_id:
            query = query.filter(Report.course_id == course_id)
        if trimester_id:
            query = query.filter(Report.trimestre_id == trimester_id)
        if semester_id:
            query = query.filter(Report.semester_id == semester_id)

        query = query.group_by(Report.course_id, Report.trimestre_id, Course.name).all()

        statistics = {"courses": [], "general": {}}
        courses_dict = {}
        total_incidencias_trimestre = {}
        total_incidencias_general = 0  # Total de incidencias en todos los trimestres

        for data in query:
            course_id = data.course_id
            course_name = data.course_name
            total_incidencias = data.total_incidencias or 0

            trimester_data = {
                "trimestre_id": data.trimestre_id,
                "total_incidencias": total_incidencias,
            }

            if course_id not in courses_dict:
                courses_dict[course_id] = {
                    "course_id": course_id,
                    "course_name": course_name,
                    "trimesters": []
                }

            courses_dict[course_id]["trimesters"].append(trimester_data)

            # Acumular totales por trimestre
            if data.trimestre_id not in total_incidencias_trimestre:
                total_incidencias_trimestre[data.trimestre_id] = 0
            total_incidencias_trimestre[data.trimestre_id] += total_incidencias

            # Acumular el total de incidencias generales
            total_incidencias_general += total_incidencias

        statistics["courses"] = list(courses_dict.values())

        # Calcular índice total por trimestre
        indice_por_trimestre = {
            trimester: (total / TOTAL_ESTUDIANTES_STATIC) * 100 if TOTAL_ESTUDIANTES_STATIC > 0 else 0
            for trimester, total in total_incidencias_trimestre.items()
        }

        # Calcular índice general sobre la suma de incidencias de todos los trimestres
        indice_general = (total_incidencias_general / (TOTAL_ESTUDIANTES_STATIC * 3)) * 100 if TOTAL_ESTUDIANTES_STATIC > 0 else 0

        # Asignar los datos a la clave "general" en el JSON final
        statistics["general"] = {
            "total_incidencias_por_trimestre": total_incidencias_trimestre,
            "indice_por_trimestre": indice_por_trimestre,
            "total_incidencias_general": total_incidencias_general,
            "indice_general": indice_general
        }

        return statistics

        
    @staticmethod
    def register_nota_status(data):
        try:
            registros = []
            for registro in data.get('registros', []):
                if registro.get('indicator_id') == 14:  # Only process if indicator_id is 14
                    nuevo_registro = Evaluation(
                        indicator_id=registro.get('indicator_id'),
                        trimestre_id=registro.get('trimestre_id'),
                        course_id=registro.get('course_id'),
                        period_id=registro.get('period_id'),
                        teacher_id=registro.get('teacher_id'),
                        state_id=registro.get('state_id')  # Este es el ID del estado desde IndicatorState
                    )
                    registros.append(nuevo_registro)
                    db.session.add(nuevo_registro)

            db.session.commit()
            return {"message": "Estados de registro de notas guardados exitosamente"}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @staticmethod
    def get_nota_status(filters):
        """
        Obtiene los estados de registro de notas según los filtros proporcionados
        """
        try:
            query = Evaluation.query.filter(Evaluation.indicator_id == 14)  # Filtrar solo por indicator_id 14

            if filters.get('trimestre_id'):
                query = query.filter(Evaluation.trimestre_id == filters['trimestre_id'])
            if filters.get('course_id'):
                query = query.filter(Evaluation.course_id == filters['course_id'])
            if filters.get('period_id'):
                query = query.filter(Evaluation.period_id == filters['period_id'])
            if filters.get('teacher_id'):
                query = query.filter(Evaluation.teacher_id == filters['teacher_id'])

            registros = query.all()
            
            result = []
            for registro in registros:
                result.append({
                    "id": registro.id,
                    "indicator_id": registro.indicator_id,
                    "trimestre_id": registro.trimestre_id,
                    "course_id": registro.course_id,
                    "period_id": registro.period_id,
                    "teacher_id": registro.teacher_id,
                    "state_id": registro.state_id,
                    "state_name": registro.state.name if registro.state else None
                })

            return {"registros": result}, 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_statistics(filters):
        """
        Obtiene estadísticas de los estados de registro de notas, considerando ciertos estados como entregados.
        """
        try:
            # Define los estados que se considerarán como "entregados"
            delivered_states = ['si', 'incompleto', 'retraso']
            
            # Construir la consulta
            query = db.session.query(
                Evaluation.trimestre_id,
                Evaluation.period_id,  # Incluimos el periodo
                db.func.sum(
                    db.case(
                        (Evaluation.state_id == 'si', 1),  # Contar como entregado
                        (Evaluation.state_id == 'incompleto', 1),  # Contar como entregado
                        (Evaluation.state_id == 'retraso', 1),  # Contar como entregado
                        else_=0  # En caso contrario, contar como no entregado
                    )
                ).label('delivered_count'),  # Conteo de entregados
                db.func.count(Evaluation.id).label('total_count')  # Conteo total
            ).join(IndicatorState).filter(Evaluation.indicator_id == 14)  # Filtrar solo por indicator_id 14

            # Filtrar por los parámetros proporcionados
            if filters.get('trimestre_id'):
                query = query.filter(Evaluation.trimestre_id == filters['trimestre_id'])
            if filters.get('period_id'):
                query = query.filter(Evaluation.period_id == filters['period_id'])

            # Agrupar por trimestre y periodo
            stats = query.group_by(Evaluation.trimestre_id, Evaluation.period_id).all()

            # Estructura del resultado
            result = {
                "total_registros": sum(stat.total_count for stat in stats),
                "por_trimestre": [
                    {
                        **({"trimestre_id": stat.trimestre_id} if stat.trimestre_id is not None else {}),
                        **({"period_id": stat.period_id} if stat.period_id is not None else {}),
                        "delivered_count": stat.delivered_count,
                        "not_delivered_count": stat.total_count - stat.delivered_count,
                        "percentage_delivered": round((stat.delivered_count * 100) / stat.total_count, 2) if stat.total_count > 0 else 0,
                        "percentage_not_delivered": round(((stat.total_count - stat.delivered_count) * 100) / stat.total_count, 2) if stat.total_count > 0 else 0
                    }
                    for stat in stats
                ]
            }

            return result, 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 400
        
    @staticmethod
    def register_communications(data):
        communications = data.get("communications", [])
        for communication in communications:
            indicator_id = communication.get("indicator_id")
            trimestre_id = communication.get("trimestre_id")
            course_id = communication.get("course_id")
            teacher_id = communication.get("teacher_id")
            user_id = communication.get("user_id")
            total_communications = communication.get("communication", 0)
            
            # Construcción dinámica de filtro, omitimos campos opcionales no definidos
            filter_args = {
                "indicator_id": indicator_id,
                "trimestre_id": trimestre_id,
                "course_id": course_id
            }
            if teacher_id:
                filter_args["teacher_id"] = teacher_id
            if user_id:
                filter_args["user_id"] = user_id

            # Consultar el reporte existente o crear uno nuevo
            report = Report.query.filter_by(**filter_args).first()
            
            if report:
                report.communication = total_communications
            else:
                report = Report(
                    indicator_id=indicator_id,
                    trimestre_id=trimestre_id,
                    course_id=course_id,
                    teacher_id=teacher_id,
                    user_id=user_id,
                    communication=total_communications
                )
                db.session.add(report)

        db.session.commit()
        return {"message": "Comunicados registrados con éxito."}

    # Consultar estadísticas de comunicados
    @staticmethod
    def get_communication_statistics(course_id=None, trimestre_id=None):
        query = db.session.query(
            Report.course_id,
            Report.trimestre_id,
            func.sum(Report.communication).label("total_communications"),
            func.count(Report.id).label("total_records")
        ).filter(Report.indicator_id == 15)

        if course_id:
            query = query.filter(Report.course_id == course_id)
        if trimestre_id:
            query = query.filter(Report.trimestre_id == trimestre_id)

        query = query.group_by(Report.course_id, Report.trimestre_id).all()

        statistics = []
        for data in query:
            statistics.append({
                "course_id": data.course_id,
                "trimestre_id": data.trimestre_id,
                "total_communications": data.total_communications or 0,
                "total_records": data.total_records
            })

        return statistics