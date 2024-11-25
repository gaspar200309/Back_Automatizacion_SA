from datetime import datetime  
from app.models.peridos import db, Document

class DocumentService:
    @staticmethod
    def add_document(name, delivered, indicator_id):
        new_document = Document(
            name=name,
            delivered=delivered,
            upload_date=datetime.utcnow(),
            indicator_id=indicator_id,
        )
        db.session.add(new_document)
        db.session.commit()
        return new_document

    @staticmethod
    def get_document_counts():
        total = Document.query.count()
        delivered = Document.query.filter_by(delivered=True).count()
        not_delivered = total - delivered
        return {'total': total, 'delivered': delivered, 'not_delivered': not_delivered}

    @staticmethod
    def list_delivered_documents():
        return Document.query.all()
