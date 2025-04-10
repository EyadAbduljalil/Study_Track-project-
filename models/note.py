from datetime import datetime
from models.user import db

class Note(db.Model):
    """Note model for storing course notes."""
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shares = db.relationship('Sharing', backref='note', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, course_id, title, content):
        self.course_id = course_id
        self.title = title
        self.content = content
    
    def __repr__(self):
        return f'<Note {self.title}>'
