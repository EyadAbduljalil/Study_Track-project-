import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime

from config import config
from models import db, User, Course, Task, Note, Sharing

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from routes.courses import courses as courses_blueprint
    app.register_blueprint(courses_blueprint)
    
    from routes.tasks import tasks as tasks_blueprint
    app.register_blueprint(tasks_blueprint)
    
    from routes.notes import notes as notes_blueprint
    app.register_blueprint(notes_blueprint)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db, User=User, Course=Course, Task=Task, Note=Note, Sharing=Sharing)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
