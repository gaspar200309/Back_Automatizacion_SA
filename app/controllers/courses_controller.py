from flask import Blueprint, jsonify
from app.service.courses_service import get_all_courses, get_courses_by_teacher_id

courses_bp = Blueprint('courses_bp', __name__)

@courses_bp.route('/courses', methods=['GET'])
def list_courses():
    courses = get_all_courses()
    return jsonify(courses), 200


@courses_bp.route('/teachers/<int:teacher_id>/courses', methods=['GET'])
def get_courses_by_teacher(teacher_id):
    courses, error = get_courses_by_teacher_id(teacher_id)
    
    if error:
        return jsonify({"error": error}), 404

    # Format the courses data as JSON
    courses_data = [
        {
            "id": course.id,
            "name": course.name,
            "paralelo": course.paralelo,
            "name_paralelo": course.name_paralelo,
            "nivel": {
                "id": course.nivel.id,
                "name": course.nivel.name
            }
        } for course in courses
    ]
    
    return jsonify({"courses": courses_data}), 200