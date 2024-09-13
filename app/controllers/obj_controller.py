from flask import Blueprint, jsonify
from app.service.obj_service import get_academic_objectives, get_sgc_objectives

objective_bp = Blueprint('objective', __name__)

@objective_bp.route('/academic', methods=['GET'])
def list_academic_objectives():
    objectives = get_academic_objectives()
    return jsonify([{'id': obj.id, 'name': obj.name} for obj in objectives])

@objective_bp.route('/sgc-objectives', methods=['GET'])
def list_sgc_objectives():
    objectives = get_sgc_objectives()
    return jsonify([{'id': obj.id, 'name': obj.name} for obj in objectives])