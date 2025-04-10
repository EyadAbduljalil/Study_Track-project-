from datetime import datetime
from models.user import db

class Course(db.Model):
    """Course model for storing course information."""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20))
    instructor = db.Column(db.String(100))
    color = db.Column(db.String(20), default='#3498db')  # Default blue color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    notes = db.relationship('Note', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, user_id, title, code=None, instructor=None, color=None):
        self.user_id = user_id
        self.title = title
        self.code = code
        self.instructor = instructor
        self.color = color or '#3498db'
    
    def __repr__(self):
        return f'<Course {self.title}>'
