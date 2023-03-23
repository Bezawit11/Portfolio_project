from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = '91a8a09976b50c34691ba6158b768c64'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'app_auth.login'
    login_manager.session_protection = 'strong'

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .views import app_views
    from .auth import app_auth

    app.register_blueprint(app_views, url_prefix='/')
    app.register_blueprint(app_auth, url_prefix='/')

    from .models import User, Item
    with app.app_context():
        db.create_all()

    return app

