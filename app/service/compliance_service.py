from sqlalchemy.exc import IntegrityError  
from sqlalchemy.orm import joinedload 
from app.models.Indicadores import db, Evaluation, Indicator, IndicatorState
from app.models.user import Teacher


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


from sqlalchemy.orm import joinedload

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
