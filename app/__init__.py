from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
session = Session()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    session.init_app(app)

    # Set up login manager
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        # Import models
        from . import models
        
        # Import routes
        from .auth import bp as auth_bp
        from .dashboard import bp as dashboard_bp
        from .api import bp as api_bp
        
        # Register blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(api_bp, url_prefix='/api')
        
        # Create database tables
        db.create_all()
        
        @app.route('/')
        def index():
            from flask import redirect, url_for
            return redirect(url_for('auth.login'))
        
        return app 