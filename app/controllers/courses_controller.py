from flask import Blueprint, jsonify
from app.service.courses_service import get_all_courses

courses_bp = Blueprint('courses_bp', __name__)

@courses_bp.route('/courses', methods=['GET'])
def list_courses():
    courses = get_all_courses()
    return jsonify(courses), 200
