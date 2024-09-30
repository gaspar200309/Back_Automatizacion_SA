from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import db, Document
from .services import DocumentService

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/documents', methods=['POST'])
def create_document():
    data = request.get_json()
    name = data.get('name')
    delivered = data.get('delivered')
    indicator_id = data.get('indicator_id')
    period_id = data.get('period_id')

    new_document = DocumentService.add_document(name, delivered, indicator_id, period_id)
    return jsonify({'message': 'Documento creado exitosamente', 'document': new_document.serialize()}), 201

@documents_bp.route('/documents/counts', methods=['GET'])
def get_counts():
    counts = DocumentService.get_document_counts()
    return jsonify(counts), 200

@documents_bp.route('/documents/delivered', methods=['GET'])
def get_delivered_documents():
    documents = DocumentService.list_delivered_documents()
    return jsonify([doc.serialize() for doc in documents]), 200
