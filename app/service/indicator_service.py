from app.models.Indicadores import Indicator, Evaluation, IndicatorState, DeliveryDeadline, PeriodType
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from app.models.user import User, Teacher
from app import db

class IndicatorService:
    @staticmethod
    def create_indicator(data):
        """
        Crea un indicador y sus plazos de entrega. 
        Optimizado para reducir transacciones innecesarias.
        """
        print("Datos recibidos para crear el indicador:", data)
        try:
            # Crear el indicador
            indicator = Indicator(
                name=data.get('name'),
                improvement_action=data.get('improvement_action'),
                expected_result=data.get('expected_result'),
                academic_objective_id=data.get('academic_objective_id'),
                sgc_objective_id=data.get('sgc_objective_id'),
                formula_id=data.get('formula_id'),
            )
            db.session.add(indicator)

            # Crear los plazos de entrega
            deadlines_data = data.get('deadlines', [])
            deadlines = [
                DeliveryDeadline(
                    delivery_date=dl.get('delivery_date'),
                    period_type=PeriodType(dl.get('period_type')),
                    indicator=indicator
                ) for dl in deadlines_data
            ]
            db.session.add_all(deadlines)

            db.session.commit()

            # Respuesta formateada
            return {
                'id': indicator.id,
                'name': indicator.name,
                'deadlines': [{'delivery_date': d.delivery_date, 'period_type': d.period_type.value} for d in deadlines]
            }
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear el indicador: {str(e)}")

    @staticmethod
    def get_all_indicators(limit=None, offset=None):
        try:
            query = db.session.query(Indicator.id, Indicator.name)
            if limit is not None and offset is not None:
                query = query.limit(limit).offset(offset)
            indicators = query.all()
            return [{'id': ind.id, 'name': ind.name} for ind in indicators]
        except Exception as e:
            raise Exception(f"Error retrieving indicators: {str(e)}")
    
    @staticmethod
    def assign_coordinator(indicator_id, user_id):
        """
        Asigna un coordinador a un indicador.
        """
        try:
            indicator = db.session.query(Indicator).get(indicator_id)
            user = db.session.query(User).get(user_id)

            if not indicator or not user:
                raise ValueError("El indicador o el usuario no existe")

            # Validar si ya está asignado
            if user in indicator.users:
                raise ValueError("El usuario ya es coordinador de este indicador")

            indicator.users.append(user)
            db.session.commit()
            return {'message': 'Coordinador asignado correctamente'}
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al asignar coordinador: {str(e)}")

    @staticmethod
    def remove_coordinator(indicator_id, user_id):
        """
        Desasigna un coordinador de un indicador.
        """
        try:
            indicator = db.session.query(Indicator).get(indicator_id)
            user = db.session.query(User).get(user_id)

            if not indicator or not user:
                raise ValueError("El indicador o el usuario no existe")

            if user not in indicator.users:
                raise ValueError("El usuario no está asignado como coordinador")

            indicator.users.remove(user)
            db.session.commit()
            return {'message': 'Coordinador desasignado correctamente'}
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al desasignar coordinador: {str(e)}")

    @staticmethod
    def count_indicators():
        """
        Cuenta los indicadores y clasifica su estado.
        """
        try:
            total = db.session.query(func.count(Indicator.id)).scalar()
            completed = db.session.query(func.count(Indicator.id)).filter(Indicator.is_completed == True).scalar()
            incomplete = total - completed

            return {'total': total, 'completed': completed, 'incomplete': incomplete}
        except Exception as e:
            raise Exception(f"Error counting indicators: {str(e)}")

    @staticmethod
    def get_indicators_by_username(username):
        """
        Recupera indicadores asociados a un usuario.
        """
        try:
            user = db.session.query(User).options(joinedload(User.indicators)).filter_by(username=username).first()

            if not user:
                raise ValueError("Usuario no encontrado")

            return [{
                'id': ind.id,
                'name': ind.name,
                'is_completed': ind.is_completed,
                'improvement_action': ind.improvement_action,
                'expected_result': ind.expected_result,
                'academic_objective': ind.academic_objective.name if ind.academic_objective else None,
                'sgc_objective': ind.sgc_objective.name if ind.sgc_objective else None,
                'formula': ind.formula.formula if ind.formula else None
            } for ind in user.indicators]
        except Exception as e:
            raise Exception(f"Error retrieving indicators for user: {str(e)}")

    @staticmethod
    def register_compliance(indicator_id, teacher_name, state_name):
        """
        Registra el cumplimiento de un indicador para un profesor y estado dado.
        """
        try:
            indicator = Indicator.query.get(indicator_id)
            if not indicator:
                raise ValueError("Indicador no encontrado")

            name, last_name = teacher_name.split(' ', 1)
            teacher = Teacher.query.filter_by(name=name, last_name=last_name).first()
            if not teacher:
                raise ValueError("Profesor no encontrado")

            state = IndicatorState.query.filter_by(name=state_name).first()
            if not state:
                raise ValueError("Estado no encontrado")

            compliance = Evaluation.query.filter_by(indicator_id=indicator.id, teacher_id=teacher.id).first()
            if compliance:
                compliance.state_id = state.id
            else:
                compliance = Evaluation(indicator_id=indicator.id, teacher_id=teacher.id, state_id=state.id)
                db.session.add(compliance)

            db.session.commit()
            return {'message': 'Cumplimiento registrado correctamente'}
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al registrar cumplimiento: {str(e)}")

    @staticmethod
    def get_indicator_deadlines_service():
        try:
            indicators = db.session.query(Indicator).options(
                joinedload(Indicator.users).load_only(User.name, User.photo)
            ).all()

            result = [{
                'id': indicator.id,
                'name': indicator.name,
                'is_completed': indicator.is_completed,
                'deadlines': [{
                    'delivery_date': deadline.delivery_date,
                    'period_type': deadline.period_type.value
                } for deadline in indicator.deadlines],
                'assigned_user': [{'name': user.name, 'photo': user.photo} for user in indicator.users]
            } for indicator in indicators]

            return result
        except Exception as e:
            print(f"Error al obtener fechas de entrega: {str(e)}")
            raise e

    @staticmethod
    def get_assigned_users_by_indicator(indicator_id):
        """
        Obtiene los usuarios asignados a un indicador específico.
        """
        try:
            # Buscar el indicador por ID y cargar los usuarios asignados
            indicator = db.session.query(Indicator).options(
                joinedload(Indicator.users).load_only(User.id, User.name, User.last_name, User.photo)
            ).filter_by(id=indicator_id).first()

            if not indicator:
                raise ValueError("Indicador no encontrado")

            # Formatear los datos de los usuarios
            assigned_users = [{
                'id': user.id,
                'name': f"{user.name} {user.last_name}",
                'photo': user.photo
            } for user in indicator.users]

            return assigned_users
        except Exception as e:
            print(f"Error al obtener usuarios asignados al indicador: {str(e)}")
            raise Exception(f"Error al obtener usuarios asignados: {str(e)}")
