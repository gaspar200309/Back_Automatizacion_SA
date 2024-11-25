from app import db
from app.models.Indicadores import StudentStatus, Report, IndicatorState, Evaluation
from ..models.user import User, Teacher
from app.models.coures import Course
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

class StudentStatusService:

    TOTAL_STUDENTS = 1060 

    @staticmethod
    def register_active_students(trimestre_id, active_students_count):
        inactive_students_count = StudentStatusService.TOTAL_STUDENTS - active_students_count
        
        active_percentage = (active_students_count / StudentStatusService.TOTAL_STUDENTS) * 100
        inactive_percentage = (inactive_students_count / StudentStatusService.TOTAL_STUDENTS) * 100

        student_status = StudentStatus(
            indicator_id=10, 
            trimestre_id=trimestre_id,
            active_students=active_students_count,
            inactive_students=inactive_students_count
        )

        db.session.add(student_status)
        db.session.commit()

        return {
            "trimestre_id": trimestre_id,
            "active_students": active_students_count,
            "inactive_students": inactive_students_count,
            "active_percentage": active_percentage,
            "inactive_percentage": inactive_percentage
        }

    @staticmethod
    def get_student_status(trimestre_id):
        student_status = StudentStatus.query.filter_by(trimestre_id=trimestre_id).first()
        if not student_status:
            return None

        active_percentage = (student_status.active_students / StudentStatusService.TOTAL_STUDENTS) * 100
        inactive_percentage = (student_status.inactive_students / StudentStatusService.TOTAL_STUDENTS) * 100

        return {
            "trimestre_id": trimestre_id,
            "active_students": student_status.active_students,
            "inactive_students": student_status.inactive_students,
            "active_percentage": active_percentage,
            "inactive_percentage": inactive_percentage
        }
        
    @staticmethod
    def get_all_student_statuses():
        statuses = StudentStatus.query.all()
        
        results = []
        for status in statuses:
            active_percentage = (status.active_students / StudentStatusService.TOTAL_STUDENTS) * 100
            inactive_percentage = (status.inactive_students / StudentStatusService.TOTAL_STUDENTS) * 100

            results.append({
                "trimestre_id": status.trimestre_id,
                "active_students": status.active_students,
                "inactive_students": status.inactive_students,
                "active_percentage": active_percentage,
                "inactive_percentage": inactive_percentage
            })
        
        return results

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
            if data.get('indicator_id') != 14:
                return {"error": "Solo se permite el registro para indicator_id 14"}, 400

            nuevo_registro = Evaluation(
                indicator_id=data.get('indicator_id'),
                course_id=data.get('course_id'),
                period_id=data.get('period_id'),
                teacher_id=data.get('teacher_id'),
                trimestre_id=data.get('trimestre_id'),
                state_id=data.get('state_id')
            )

            db.session.add(nuevo_registro)
            db.session.commit()
            
            return {"message": "Estado de registro de nota guardado exitosamente"}, 201
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 400


    @staticmethod
    def get_nota_status(filters):
        """
        Obtiene los estados de registro de notas según los filtros proporcionados.
        """
        try:
            query = Evaluation.query.filter(Evaluation.indicator_id == 14)  # Filtrar solo por indicator_id 14

            # Applying filters
            if filters.get('trimestre_id'):
                query = query.filter(Evaluation.trimestre_id == filters['trimestre_id'])
            if filters.get('course_id'):
                query = query.filter(Evaluation.course_id == filters['course_id'])
            if filters.get('period_id'):
                query = query.filter(Evaluation.period_id == filters['period_id'])
            if filters.get('teacher_id'):
                query = query.filter(Evaluation.teacher_id == filters['teacher_id'])

            registros = query.all()

            # Variables para cálculos generales
            delivered_count = 0
            not_delivered_count = 0
            result = []

            # Procesar cada registro
            for registro in registros:
                if registro.state_id == 1:  # Considerar '1' como entregado
                    delivered_count += 1
                else:
                    not_delivered_count += 1
                
                # Append record data, using relationships to fetch names
                result.append({
                    "id": registro.id,
                    "indicator_id": registro.indicator_id,
                    "trimestre_id": registro.trimestre_id,
                    "course_id": registro.course_id,
                    "period_id": registro.period_id,
                    "teacher_id": registro.teacher_id,
                    "state_id": registro.state_id,
                    "state_name": registro.state.name if registro.state else None,
                    "course_name": registro.course.name if registro.course else None,
                    "teacher_name": f"{registro.teacher.name} {registro.teacher.last_name}" if registro.teacher else None
                })

            # General calculations
            total_count = delivered_count + not_delivered_count
            percentage_delivered = (delivered_count / total_count * 100) if total_count > 0 else 0
            percentage_not_delivered = (not_delivered_count / total_count * 100) if total_count > 0 else 0

            # Formatear la respuesta final
            formatted_response = {
                "records": result,
                "general": {
                    "delivered_count": str(delivered_count),
                    "not_delivered_count": str(not_delivered_count),
                    "percentage_delivered": f"{percentage_delivered:.2f}",
                    "percentage_not_delivered": f"{percentage_not_delivered:.2f}"
                }
            }

            return formatted_response, 200

        except SQLAlchemyError as e:
            return {"error": str(e)}, 400

        
    @staticmethod
    def register_communications(data):
        """
        Registra las comunicaciones de un único registro.
        """
        # Obtener el objeto de comunicación directamente
        communication = data

        # Extraer los valores
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

        # Realiza el commit a la base de datos
        db.session.commit()
        return {"message": "Comunicación registrada con éxito."}

    # Consultar estadísticas de comunicados
    @staticmethod
    def get_communication_statistics(course_id=None, trimestre_id=None):
        query = (
            db.session.query(
                Report.course_id,
                Course.name.label("course_name"),  # Nombre del curso
                Report.trimestre_id,
                func.sum(Report.communication).label("total_communications"),
                func.count(Report.id).label("total_records"),
                Teacher.name.label("teacher_name"),  # Nombre del profesor
                User.name.label("user_name")  # Nombre del usuario
            )
            .outerjoin(Course, Report.course_id == Course.id)
            .outerjoin(Teacher, Report.teacher_id == Teacher.id)
            .outerjoin(User, Report.user_id == User.id)
            .filter(Report.indicator_id == 15)
        )

        if course_id:
            query = query.filter(Report.course_id == course_id)
        if trimestre_id:
            query = query.filter(Report.trimestre_id == trimestre_id)

        query = query.group_by(
            Report.course_id, 
            Course.name,
            Report.trimestre_id,
            Teacher.name,
            User.name
        ).all()

        # Transformar los resultados
        statistics = []
        for data in query:
            statistics.append({
                "course_id": data.course_id,
                "course_name": data.course_name,
                "trimestre_id": data.trimestre_id,
                "total_communications": data.total_communications or 0,
                "total_records": data.total_records,
                "teacher_name": data.teacher_name,
                "user_name": data.user_name
            })

        return statistics