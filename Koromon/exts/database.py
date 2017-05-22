from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def setup_database(app):
    db.init_app(app)
