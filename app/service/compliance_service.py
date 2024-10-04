from sqlalchemy.exc import IntegrityError  
from sqlalchemy.orm import joinedload 
from app.models.Indicadores import db, Evaluation, Indicator, IndicatorState
from app.models.peridos import Trimester, Period
from app.models.user import Teacher
from app.models.coures import Course


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

    total_count = len(evaluations)
    delivered_count = sum(1 for e in evaluations if e.state.name in ['Sí', 'Retraso', 'Incompleto'])
    not_delivered_count = total_count - delivered_count

    delivered_percentage = (delivered_count / total_count * 100) if total_count > 0 else 0
    not_delivered_percentage = (not_delivered_count / total_count * 100) if total_count > 0 else 0

    statistics = {
        'total_count': total_count,
        'delivered_count': delivered_count,
        'not_delivered_count': not_delivered_count,
        'delivered_percentage': round(delivered_percentage, 2),
        'not_delivered_percentage': round(not_delivered_percentage, 2)
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

    # Inicializar el diccionario con los nombres exactos de los trimestres
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
    
    

def create_indicator6_evaluation_service(data):
    try:
        teacher_id = data.get('teacher_id')
        course_id = data.get('course_id')
        period_id = data.get('period_id')
        paralelo = data.get('paralelo')
        percentage = data.get('percentage')

        if not all([teacher_id, course_id, period_id, paralelo, percentage]):
            return {'error': 'Todos los campos son requeridos', 'status': 400}

        teacher = Teacher.query.get(teacher_id)
        course = Course.query.get(course_id)
        period = Period.query.get(period_id)

        if not teacher or not course or not period:
            return {'error': 'Datos no válidos para profesor, curso o período', 'status': 404}

        evaluation = Evaluation(
            teacher_id=teacher_id,
            course_id=course_id,
            period_id=period_id,
            paralelo=paralelo,
            indicator_id=6,  
            percentage=percentage  
        )

        db.session.add(evaluation)
        db.session.commit()

        return {'message': 'Evaluación creada exitosamente'}

    except IntegrityError:
        db.session.rollback()
        return {'error': 'Ocurrió un error de integridad en la base de datos', 'status': 500}


def create_new_evaluation_indicator6(indicator_id, teacher_id, percentage, course_id, period_id, paralelo):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        raise ValueError(f"No se encontró el profesor con ID {teacher_id}")

    new_evaluation = Evaluation(
        indicator_id=indicator_id,
        teacher_id=teacher.id,
        course_id=course_id,
        period_id=period_id,
        paralelo=paralelo,
        percentage=percentage, 
        
    )

    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation
