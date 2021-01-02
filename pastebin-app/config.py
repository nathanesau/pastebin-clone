import os
from dotenv import load_dotenv


load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/.env")


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or \
        f"sqlite:////{os.path.dirname(os.path.realpath(__file__))}/app.db"
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'vZ9YVje1aU'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PASTES_PER_PAGE = 10
    USER_PASTES_LIMIT = 25
    PASTES_FOLDER = os.getenv('PASTES_FOLDER') or \
        f"{os.path.dirname(os.path.realpath(__file__))}/pastes"
    ALLOWED_EXTENSIONS = {'txt'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


SWAGGER_CONFIG = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/pastebin-clone/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/pastebin-clone/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/pastebin-clone/apidocs/"
}


SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "pastebin-clone api",
        "description": (
            "API docs for pastebin-clone.\n\n"
            "Set authorization header using \"Authorize\" to try out endpoints.\n\n"
        )
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": (
                "Token: 'curl --user \"username:pass\" -XPOST http://localhost:5001/pastebin-clone/api/tokens'"
                "\nExample: 'Bearer 2vYuaDza171SSXZWCFQWs9HaOpyBwK0i'"
            )
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}
