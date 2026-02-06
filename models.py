from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RPAProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Új')
    arrival_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.Date, nullable=True)
    percentage = db.Column(db.Integer, default=0)

    # Document filenames (None if not uploaded)
    doc_business = db.Column(db.String(255), nullable=True)
    doc_test = db.Column(db.String(255), nullable=True)
    doc_ops = db.Column(db.String(255), nullable=True)

    fte = db.Column(db.Float, nullable=True)
    requestor = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<RPAProject {self.id} - {self.developer_name}>'
