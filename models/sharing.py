from datetime import datetime
from models.user import db

class Sharing(db.Model):
    """Sharing model for note sharing between users."""
    __tablename__ = 'sharing'
    
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    shared_with = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, note_id, shared_with):
        self.note_id = note_id
        self.shared_with = shared_with
    
    def __repr__(self):
        return f'<Sharing note_id={self.note_id} shared_with={self.shared_with}>'
