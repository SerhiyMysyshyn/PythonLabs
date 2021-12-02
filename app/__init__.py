from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from .main_bp import main_bp
        app.register_blueprint(main_bp, url_prefix='/')

        from .auth import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .form_registerzno import registerzno_blueprint
        app.register_blueprint(registerzno_blueprint, url_prefix='/registerzno')

        from .posts import post_blueprint
        app.register_blueprint(post_blueprint, url_prefix='/post')

        return app

