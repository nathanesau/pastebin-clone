from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flasgger import Swagger
from flask_cors import CORS
from config import Config, SWAGGER_TEMPLATE, SWAGGER_CONFIG
from werkzeug.utils import secure_filename


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."
bootstrap = Bootstrap()
moment = Moment()
swagger = Swagger(template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    swagger.init_app(app)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/pastebin-clone/auth')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/pastebin-clone')
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/pastebin-clone/api')
    return app


from app import models