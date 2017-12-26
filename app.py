from extensions import db, api, ma
from settings import Config
from flask import Flask


class App:
    def __new__(cls, config_object=Config):
        app = Flask(__name__.split('.')[0])
        app.config.from_object(config_object)

        cls.register_extensions(app)

        return app

    @staticmethod
    def register_extensions(app):
        """ Initialize Database """
        # Order matters: Initialize SQLAlchemy before Marshmallow
        db.app = app
        db.init_app(app)

        """ Initialize API """
        api.app = app
        api.init_app(app)

        """ Initialize Marshmallow """
        ma.app = app
        ma.init_app(app)
