from flask import Flask
from .database import init_db

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config["DATABASE"] = "veiculos.db"

    init_db(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app
