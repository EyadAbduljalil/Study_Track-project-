import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Base configuration class."""
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-studytrack-app'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///studytrack.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for profile pictures and attachments
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    
    # Maximum file size for uploads (5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, ensure SECRET_KEY is set in environment variables
    
    # Use PostgreSQL in production
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
