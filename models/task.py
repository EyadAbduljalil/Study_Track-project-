from datetime import datetime
from models.user import db

class Task(db.Model):
    """Task model for storing task information."""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, course_id, title, due_date, description=None, priority='medium', status='pending'):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
    
    def __repr__(self):
        return f'<Task {self.title}>'
