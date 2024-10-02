from app.models.Indicadores import Indicator, Evaluation, IndicatorState
from sqlalchemy import func
from app.models.user import User, Teacher
from app import db

def create_indicator(data):
    print("Datos recibidos para crear el indicador:", data)
    try:
        indicator = Indicator(
            name=data.get('name'),
            delivery_deadline=data.get('delivery_deadline'),
            due_date=data.get('due_date'),
            improvement_action=data.get('improvement_action'),
            expected_result=data.get('expected_result'),
            academic_objective_id=data.get('academic_objective_id'),
            sgc_objective_id=data.get('sgc_objective_id'),
            formula_id=data.get('formula_id')
        )
        db.session.add(indicator)
        db.session.commit()
        return indicator
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creating indicator: {str(e)}")

def get_all_indicators():
    try:
        indicators = db.session.query(Indicator).all()
        return indicators
    except Exception as e:
        raise Exception(f"Error retrieving indicators: {str(e)}")
    
def assign_coordinator_to_indicator(indicator_id, user_id):
    try:
        indicator = db.session.query(Indicator).filter_by(id=indicator_id).first()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not indicator or not user:
            raise Exception("El indicador o el usuario no existe")

        # Asignar el usuario al indicador en la tabla intermedia
        indicator.users.append(user)
        db.session.commit()
        return {'message': 'Coordinador asignado correctamente'}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al asignar coordinador: {str(e)}")
    
def remove_coordinator_from_indicator(indicator_id, user_id):
    try:
        indicator = db.session.query(Indicator).filter_by(id=indicator_id).first()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not indicator or not user:
            raise Exception("El indicador o el usuario no existe")

        # Quitar el usuario del indicador
        indicator.users.remove(user)
        db.session.commit()
        return {'message': 'Coordinador desasignado correctamente'}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al desasignar coordinador: {str(e)}")


def count_indicators():
    total = db.session.query(func.count(Indicator.id)).scalar()
    completed = db.session.query(func.count(Indicator.id)).filter(Indicator.is_completed == True).scalar()
    incomplete = total - completed

    return {
        'total': total,
        'completed': completed,
        'incomplete': incomplete,
    }
    
def get_indicators_by_username(username):
    try:
        user = db.session.query(User).filter_by(username=username).first()

        if not user:
            raise Exception("Usuario no encontrado")

        indicators = user.indicators 

        result = []
        for indicator in indicators:
            result.append({
                'id': indicator.id,
                'name': indicator.name,
                'delivery_deadline': str(indicator.delivery_deadline),
                'due_date': str(indicator.due_date),
                'improvement_action': indicator.improvement_action,
                'expected_result': indicator.expected_result,
                'is_completed': indicator.is_completed,
                'academic_objective': indicator.academic_objective.name if indicator.academic_objective else None,
                'sgc_objective': indicator.sgc_objective.name if indicator.sgc_objective else None,
                'formula': indicator.formula.formula if indicator.formula else None
            })

        return result
    except Exception as e:
        raise Exception(f"Error retrieving indicators for user: {str(e)}")
    
def get_indicator_assignments():
    """Obtiene todos los indicadores con sus usuarios asignados"""
    try:
        indicators = db.session.query(Indicator).all()
        return [{
            'id': indicator.id,
            'name': indicator.name,
            'coordinators': [{
                'id': user.id,
                'username': user.username
            } for user in indicator.users]
        } for indicator in indicators]
    except Exception as e:
        raise Exception(f"Error retrieving indicator assignments: {str(e)}")


def register_compliance(indicator_id, teacher_name, state_name):
    try:
        # Obtener el indicador
        indicator = Indicator.query.get(indicator_id)
        if not indicator:
            raise Exception("Indicador no encontrado")

        # Obtener el profesor
        name, last_name = teacher_name.split(' ', 1)
        teacher = Teacher.query.filter_by(name=name, last_name=last_name).first()
        if not teacher:
            raise Exception("Profesor no encontrado")

        # Obtener el estado
        state = IndicatorState.query.filter_by(name=state_name).first()
        if not state:
            raise Exception("Estado no encontrado")

        # Crear o actualizar el cumplimiento
        compliance = Evaluation.query.filter_by(indicator_id=indicator.id, teacher_id=teacher.id).first()
        if compliance:
            compliance.state_id = state.id 
        else:
            compliance = Evaluation(indicator_id=indicator.id, teacher_id=teacher.id, state_id=state.id)
            db.session.add(compliance)

        db.session.commit()
        return compliance
    except Exception as e:
        db.session.rollback()
        raise e

def get_compliance(indicator_id):
    return Evaluation.query.filter_by(indicator_id=indicator_id).all()