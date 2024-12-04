from sqlalchemy.exc import IntegrityError  
from sqlalchemy.orm import joinedload 
from app.models.Indicadores import db, Evaluation, Indicator, IndicatorState
from app.models.peridos import Trimester, Period
from app.models.user import Teacher
from app.models.coures import Course

#Indicador 2
def create_new_evaluation(indicator_id, teacher_id, state_id):
    try:
        indicator = Indicator.query.get(indicator_id)
        if not indicator:
            raise ValueError(f"Indicator with id {indicator_id} does not exist")

        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            raise ValueError(f"Teacher with id {teacher_id} does not exist")

        state = IndicatorState.query.get(state_id)
        if not state:
            raise ValueError(f"IndicatorState with id {state_id} does not exist")

        evaluation = Evaluation(
            indicator_id=indicator_id,
            teacher_id=teacher_id,
            state_id=state_id
        )
        db.session.add(evaluation)
        db.session.commit()
        return evaluation
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"IntegrityError: {str(e)}")
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creating evaluation: {str(e)}")


def get_evaluations_by_indicator(indicator_id):
    return Evaluation.query.filter_by(indicator_id=indicator_id).all()

    
def get_evaluations_by_indicator(indicator_id):
    return Evaluation.query.filter_by(indicator_id=indicator_id).all()

def get_evaluation_statistics(indicator_id):
    evaluations = Evaluation.query.filter_by(indicator_id=indicator_id).all()
    total_count = len(evaluations)
    delivered_count = sum(1 for e in evaluations if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
    not_delivered_count = total_count - delivered_count
    
    delivered_percentage = (delivered_count / total_count * 100) if total_count > 0 else 0
    not_delivered_percentage = (not_delivered_count / total_count * 100) if total_count > 0 else 0
    
    return {
        'total_count': total_count,
        'delivered_count': delivered_count,
        'not_delivered_count': not_delivered_count,
        'delivered_percentage': round(delivered_percentage, 2),
        'not_delivered_percentage': round(not_delivered_percentage, 2)
    }


#Indicador 2
def get_all_evaluations_with_details(indicator_id):
    evaluations = Evaluation.query.options(
        joinedload(Evaluation.teacher),
        joinedload(Evaluation.state),
        joinedload(Evaluation.indicator)
    ).filter(Evaluation.indicator_id == indicator_id).all()

    evaluation_data = [{
        'id': e.id,
        'indicator_name': e.indicator.name,
        'teacher': {
            'id': e.teacher.id,
            'name': e.teacher.name,
            'last_name': e.teacher.last_name,
            'asignatura': e.teacher.asignatura
        },
        'state': {
            'id': e.state.id,
            'name': e.state.name
        }
    } for e in evaluations]

    # Contamos las ocurrencias de cada estado
    state_counts = {
        'Sí': 0,
        'No': 0,
        'Retraso': 0,
        'No corresponde': 0,
        'Incompleto': 0
    }

    for e in evaluations:
        state_name = e.state.name
        if state_name in state_counts:
            state_counts[state_name] += 1

    total_count = len(evaluations)
    delivered_count = state_counts['Sí'] + state_counts['Retraso'] + state_counts['Incompleto']
    not_delivered_count = state_counts['No'] + state_counts['No corresponde']

    delivered_percentage = (delivered_count / total_count * 100) if total_count > 0 else 0
    not_delivered_percentage = (not_delivered_count / total_count * 100) if total_count > 0 else 0

    statistics = {
        'total_count': total_count,
        'delivered_count': delivered_count,
        'not_delivered_count': not_delivered_count,
        'delivered_percentage': round(delivered_percentage, 2),
        'not_delivered_percentage': round(not_delivered_percentage, 2),
        'state_counts': state_counts  # Añadimos los conteos de cada estado
    }

    return evaluation_data, statistics



def create_new_evaluation_with_trimester(indicator_id, teacher_id, trimestre_id, state_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError(f"No se encontró el profesor con ID {teacher_id}")

    trimester = Trimester.query.get(trimestre_id)
    if not trimester:
        raise ValueError(f"No se encontró el trimestre con ID {trimestre_id}")

    state = IndicatorState.query.get(state_id)
    if not state:
        raise ValueError(f"No se encontró el estado con ID {state_id}")

    new_evaluation = Evaluation(
        indicator_id=indicator_id,
        teacher_id=teacher.id,
        trimestre_id=trimester.id,
        state_id=state.id,
    )

    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation


#"Indicator 4" Obtiene todos los datos del indicador 4
def get_all_with_details_indicator4(indicator_id):
    evaluations = Evaluation.query.options(
        joinedload(Evaluation.teacher),
        joinedload(Evaluation.state),
        joinedload(Evaluation.indicator),
        joinedload(Evaluation.trimestre)
    ).filter(Evaluation.indicator_id == indicator_id).all()
    
    print(f"Total evaluations retrieved: {len(evaluations)}")  # Debug
    
    evaluation_data = [{
        'id': e.id,
        'indicator_name': e.indicator.name,
        'teacher': {
            'id': e.teacher.id,
            'name': e.teacher.name,
            'last_name': e.teacher.last_name,
            'asignatura': e.teacher.asignatura
        },
        'state': {
            'id': e.state.id,
            'name': e.state.name
        },
        'trimester': {
            'id': e.trimestre.id,
            'name': e.trimestre.name
        },
    } for e in evaluations]

    trimester_stats = {}
    for e in evaluations:
        trimester_name = e.trimestre.name.strip()
        if trimester_name not in trimester_stats:
            trimester_stats[trimester_name] = []
        trimester_stats[trimester_name].append(e)
    
    statistics_by_trimester = {}
    for trimester, evals in trimester_stats.items():
        total_count = len(evals)
        delivered_count = sum(1 for e in evals if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
        not_delivered_count = total_count - delivered_count
        
        delivered_percentage = (delivered_count / total_count * 100) if total_count > 0 else 0
        not_delivered_percentage = (not_delivered_count / total_count * 100) if total_count > 0 else 0
        
        statistics_by_trimester[trimester] = {
            'total_count': total_count,
            'delivered_count': delivered_count,
            'not_delivered_count': not_delivered_count,
            'delivered_percentage': round(delivered_percentage, 2),
            'not_delivered_percentage': round(not_delivered_percentage, 2)
        }
    
    # Calcular estadísticas generales
    overall_total_count = len(evaluations)
    overall_delivered_count = sum(1 for e in evaluations if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
    overall_not_delivered_count = overall_total_count - overall_delivered_count
    
    overall_delivered_percentage = (overall_delivered_count / overall_total_count * 100) if overall_total_count > 0 else 0
    overall_not_delivered_percentage = (overall_not_delivered_count / overall_total_count * 100) if overall_total_count > 0 else 0
    
    overall_statistics = {
        'total_count': overall_total_count,
        'delivered_count': overall_delivered_count,
        'not_delivered_count': overall_not_delivered_count,
        'delivered_percentage': round(overall_delivered_percentage, 2),
        'not_delivered_percentage': round(overall_not_delivered_percentage, 2)
    }
    
    return evaluation_data, {
        'statistics_by_trimester': statistics_by_trimester,
        'overall_statistics': overall_statistics
    }
    
#Obtiene las estadisticas del indicador 4
def get_statistics_by_trimester_and_indicator(indicator_id, trimestre_id):
    evaluations = Evaluation.query.options(
        joinedload(Evaluation.teacher),
        joinedload(Evaluation.state),
        joinedload(Evaluation.indicator),
        joinedload(Evaluation.trimestre)
    ).filter(
        Evaluation.indicator_id == indicator_id,
        Evaluation.trimestre_id == trimestre_id
    ).all()

    delivered_count = sum(1 for e in evaluations if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
    not_delivered_count = len(evaluations) - delivered_count

    # Conteo por estado
    state_counts = {}
    for e in evaluations:
        state_name = e.state.name.strip()
        state_counts[state_name] = state_counts.get(state_name, 0) + 1

    return {
        'delivered_count': delivered_count,
        'not_delivered_count': not_delivered_count,
        'state_counts': state_counts
    }


def create_indicator6_evaluation_service(data):
    from sqlalchemy.exc import IntegrityError

    try:
        # Validación inicial
        if not all(isinstance(item, dict) for item in data):
            return {'error': 'Datos inválidos: cada registro debe ser un objeto', 'status': 400}

        # Extraer IDs únicos para validación en bloque
        teacher_ids = {item.get('teacher_id') for item in data if 'teacher_id' in item}
        course_ids = {item.get('course_id') for item in data if 'course_id' in item}
        period_ids = {item.get('period_id') for item in data if 'period_id' in item}

        # Verificar existencia de IDs en la base de datos
        teachers = {t.id for t in Teacher.query.filter(Teacher.id.in_(teacher_ids)).all()}
        courses = {c.id for c in Course.query.filter(Course.id.in_(course_ids)).all()}
        periods = {p.id for p in Period.query.filter(Period.id.in_(period_ids)).all()}

        # Preparar evaluaciones
        evaluations = []
        for item in data:
            teacher_id = item.get('teacher_id')
            course_id = item.get('course_id')
            period_id = item.get('period_id')
            percentage = item.get('percentage')

            # Validar campos requeridos
            if not all([teacher_id, course_id, period_id, percentage]):
                return {'error': 'Faltan datos requeridos', 'status': 400}

            # Validar existencia en base de datos
            if teacher_id not in teachers or course_id not in courses or period_id not in periods:
                return {'error': f'Datos inválidos: {item}', 'status': 404}

            # Crear evaluación
            evaluation = Evaluation(
                teacher_id=teacher_id,
                course_id=course_id,
                period_id=period_id,
                indicator_id=6,
                porcentage=percentage
            )
            evaluations.append(evaluation)

        # Guardar evaluaciones en una sola transacción
        db.session.add_all(evaluations)
        db.session.commit()

        return {'message': 'Evaluaciones creadas exitosamente', 'status': 201}

    except IntegrityError as e:
        db.session.rollback()
        return {'error': f'Error de integridad: {str(e)}', 'status': 500}
    except Exception as e:
        db.session.rollback()
        return {'error': f'Error inesperado: {str(e)}', 'status': 500}

    
def get_estadistic_indicator6(indicator_id):
    # Obtener todas las evaluaciones relacionadas al indicador con carga diferida
    evaluations = (
        Evaluation.query.options(
            joinedload(Evaluation.teacher),
            joinedload(Evaluation.period),
        )
        .filter(Evaluation.indicator_id == indicator_id)
        .all()
    )

    stats = {}
    total_percentage_all = 0  # Para calcular el total de totales
    total_count_all = 0      # Para calcular el total de evaluaciones

    for evaluation in evaluations:
        teacher_name = f"{evaluation.teacher.name} {evaluation.teacher.last_name}" if evaluation.teacher else "Desconocido"
        period_id = evaluation.period.id if evaluation.period else "Desconocido"

        if teacher_name not in stats:
            stats[teacher_name] = {
                "teacher_name": teacher_name,
                "periods": {},
                "total_percentage": 0,
                "total_count": 0,
            }

        if period_id not in stats[teacher_name]["periods"]:
            stats[teacher_name]["periods"][period_id] = {
                "total_percentage": 0,
                "evaluation_count": 0,
            }

        # Actualizar estadísticas por periodo y profesor
        stats[teacher_name]["periods"][period_id]["total_percentage"] += evaluation.porcentage
        stats[teacher_name]["periods"][period_id]["evaluation_count"] += 1
        stats[teacher_name]["total_percentage"] += evaluation.porcentage
        stats[teacher_name]["total_count"] += 1

        # Acumular totales globales
        total_percentage_all += evaluation.porcentage
        total_count_all += 1

    # Calcular promedios por profesor y periodo
    results = []
    for teacher_name, data in stats.items():
        teacher_data = {
            "teacher_name": teacher_name,
            "periods": {},
            "overall_average": round(
                data["total_percentage"] / data["total_count"], 2
            ) if data["total_count"] > 0 else 0,
        }

        for period_id, period_data in data["periods"].items():
            teacher_data["periods"][period_id] = round(
                period_data["total_percentage"] / period_data["evaluation_count"], 2
            ) if period_data["evaluation_count"] > 0 else 0

        results.append(teacher_data)

    # Calcular promedio general
    overall_average_all = (
        round(total_percentage_all / total_count_all, 2) if total_count_all > 0 else 0
    )

    # Agregar total de totales y promedio general
    summary = {
        "total_percentage_all": total_percentage_all,
        "total_count_all": total_count_all,
        "overall_average_all": overall_average_all,
    }

    return {"results": results, "summary": summary}





def get_estadistic_indicator6_by_period(indicator_id, period_id):
    try:
        stats = db.session.query(
            Evaluation.course_id,
            Course.name.label('course_name'),
            Evaluation.porcentage.label('percentage')
        ).join(Course, Evaluation.course_id == Course.id).filter(
            Evaluation.indicator_id == indicator_id,
            Evaluation.period_id == period_id
        ).all()

        print(f"Generated stats: {stats}")
        return [{'course_name': stat.course_name, 'percentage': stat.percentage} for stat in stats]
    except Exception as e:
        import traceback
        print("Error en get_estadistic_indicator6_by_period:", traceback.format_exc())
        raise Exception(f"Error al obtener estadísticas: {str(e)}")


def create_new_evaluation_with_period(indicator_id, teacher_id, period_id, state_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError(f"No se encontró el profesor con ID {teacher_id}")

    period = Period.query.get(period_id)
    if not period:
        raise ValueError(f"No se encontró el periodo con ID {period_id}")

    state = IndicatorState.query.get(state_id)
    if not state:
        raise ValueError(f"No se encontró el estado con ID {state_id}")

    new_evaluation = Evaluation(
        indicator_id=indicator_id,
        teacher_id=teacher.id,
        period_id=period.id,
        state_id=state.id,
    )

    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation

def get_all_with_details_indicator7(indicator_id):
    evaluations = Evaluation.query.options(
        joinedload(Evaluation.teacher),
        joinedload(Evaluation.state),
        joinedload(Evaluation.indicator),
        joinedload(Evaluation.period)
    ).filter(Evaluation.indicator_id == indicator_id).all()
    
    print(f"Total evaluations retrieved: {len(evaluations)}")  # Debug
    
    evaluation_data = [{
        'id': e.id,
        'indicator_name': e.indicator.name,
        'teacher': {
            'id': e.teacher.id,
            'name': e.teacher.name,
            'last_name': e.teacher.last_name,
            'asignatura': e.teacher.asignatura
        },
        'state': {
            'id': e.state.id,
            'name': e.state.name
        },
        'period': {
            'id': e.period.id,
            'name': e.period.name
        },
    } for e in evaluations]

    period_stats = {}
    for e in evaluations:
        period_name = e.period.name.strip()
        if period_name not in period_stats:
            period_stats[period_name] = []
        period_stats[period_name].append(e)
    
    statistics_by_period = {}
    for period, evals in period_stats.items():
        total_count = len(evals)
        delivered_count = sum(1 for e in evals if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
        not_delivered_count = total_count - delivered_count
        
        delivered_percentage = (delivered_count / total_count * 100) if total_count > 0 else 0
        not_delivered_percentage = (not_delivered_count / total_count * 100) if total_count > 0 else 0
        
        statistics_by_period[period] = {
            'total_count': total_count,
            'delivered_count': delivered_count,
            'not_delivered_count': not_delivered_count,
            'delivered_percentage': round(delivered_percentage, 2),
            'not_delivered_percentage': round(not_delivered_percentage, 2)
        }
    
    # Calcular estadísticas generales
    overall_total_count = len(evaluations)
    overall_delivered_count = sum(1 for e in evaluations if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
    overall_not_delivered_count = overall_total_count - overall_delivered_count
    
    overall_delivered_percentage = (overall_delivered_count / overall_total_count * 100) if overall_total_count > 0 else 0
    overall_not_delivered_percentage = (overall_not_delivered_count / overall_total_count * 100) if overall_total_count > 0 else 0
    
    overall_statistics = {
        'total_count': overall_total_count,
        'delivered_count': overall_delivered_count,
        'not_delivered_count': overall_not_delivered_count,
        'delivered_percentage': round(overall_delivered_percentage, 2),
        'not_delivered_percentage': round(overall_not_delivered_percentage, 2)
    }
    
    return evaluation_data, {
        'statistics_by_period': statistics_by_period,
        'overall_statistics': overall_statistics
    }


def create_indicator8_period(indicator_id, teacher_id, period_id, state_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError(f"No se encontró el profesor con ID {teacher_id}")

    period = Period.query.get(period_id)
    if not period:
        raise ValueError(f"No se encontró el periodo con ID {period_id}")

    state = IndicatorState.query.get(state_id)
    if not state:
        raise ValueError(f"No se encontró el estado con ID {state_id}")

    new_evaluation = Evaluation(
        indicator_id=indicator_id,
        teacher_id=teacher.id,
        period_id=period.id,
        state_id=state.id,
    )

    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation

def get_all_with_details_indicator8(indicator_id):
    evaluations = Evaluation.query.options(
        joinedload(Evaluation.teacher),
        joinedload(Evaluation.state),
        joinedload(Evaluation.indicator),
        joinedload(Evaluation.period)
    ).filter(Evaluation.indicator_id == indicator_id).all()
    
    print(f"Total evaluations retrieved: {len(evaluations)}")  # Debug
    
    evaluation_data = [{
        'id': e.id,
        'indicator_name': e.indicator.name,
        'teacher': {
            'id': e.teacher.id,
            'name': e.teacher.name,
            'last_name': e.teacher.last_name,
            'asignatura': e.teacher.asignatura
        },
        'state': {
            'id': e.state.id,
            'name': e.state.name
        },
        'period': {
            'id': e.period.id,
            'name': e.period.name
        },
    } for e in evaluations]

    period_stats = {}
    for e in evaluations:
        period_name = e.period.name.strip()
        if period_name not in period_stats:
            period_stats[period_name] = []
        period_stats[period_name].append(e)
    
    statistics_by_period = {}
    for period, evals in period_stats.items():
        total_count = len(evals)
        delivered_count = sum(1 for e in evals if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
        not_delivered_count = total_count - delivered_count
        
        delivered_percentage = (delivered_count / total_count * 100) if total_count > 0 else 0
        not_delivered_percentage = (not_delivered_count / total_count * 100) if total_count > 0 else 0
        
        statistics_by_period[period] = {
            'total_count': total_count,
            'delivered_count': delivered_count,
            'not_delivered_count': not_delivered_count,
            'delivered_percentage': round(delivered_percentage, 2),
            'not_delivered_percentage': round(not_delivered_percentage, 2)
        }
    
    # Calcular estadísticas generales
    overall_total_count = len(evaluations)
    overall_delivered_count = sum(1 for e in evaluations if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
    overall_not_delivered_count = overall_total_count - overall_delivered_count
    
    overall_delivered_percentage = (overall_delivered_count / overall_total_count * 100) if overall_total_count > 0 else 0
    overall_not_delivered_percentage = (overall_not_delivered_count / overall_total_count * 100) if overall_total_count > 0 else 0
    
    overall_statistics = {
        'total_count': overall_total_count,
        'delivered_count': overall_delivered_count,
        'not_delivered_count': overall_not_delivered_count,
        'delivered_percentage': round(overall_delivered_percentage, 2),
        'not_delivered_percentage': round(overall_not_delivered_percentage, 2)
    }
    
    return evaluation_data, {
        'statistics_by_period': statistics_by_period,
        'overall_statistics': overall_statistics
    }

