from flask import Blueprint, jsonify
from ..service.stadistic_service import SummaryService

summary_bp = Blueprint('summary_bp', __name__)

@summary_bp.route('/summary/count', methods=['GET'])
def get_summary_counts():
    try:
        summary_counts = SummaryService.get_summary_counts()
        return jsonify(summary_counts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
