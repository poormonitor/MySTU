from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    from . import user, student, log

    db.init_app(app)
    return db
