from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.peridos import db, Document
from app.service.document_service import DocumentService

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/documents', methods=['POST'])
def create_document():
    data = request.get_json()
    name = data.get('name')
    delivered = data.get('delivered')
    indicator_id = data.get('indicator_id')

    new_document = DocumentService.add_document(name, delivered, indicator_id)
    return jsonify({'message': 'Documento creado exitosamente'}), 201

@documents_bp.route('/documents/counts', methods=['GET'])
def get_counts():
    counts = DocumentService.get_document_counts()
    return jsonify(counts), 200

@documents_bp.route('/documents/delivered', methods=['GET'])
def get_delivered_documents():
    documents = DocumentService.list_delivered_documents()
    
    documents_list = []
    for doc in documents:
        documents_list.append({
            'id': doc.id,
            'name': doc.name,
            'delivered': doc.delivered,
            'upload_date': doc.upload_date.strftime('%Y-%m-%d'),  
            'indicator_id': doc.indicator_id
        })
    
    return jsonify(documents_list), 200

