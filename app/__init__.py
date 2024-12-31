from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.auth_start'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from . import cli
    cli.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('auth.auth_start'))

    with app.app_context():
        db.create_all()

    return app

from app import models 