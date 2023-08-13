# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 10:07
# @Author  : Johnson Sun (@poormonitor)
# @Email   : poormonitor@outlook.com
# @File    : app.py

from flask import Flask
from models import init_app as models_init_app
from routes import init_app as routes_init_app
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)

    CORS(app)
    JWTManager(app)

    app.config.from_object("config.Config")

    db = models_init_app(app)
    routes_init_app(app)

    database = os.path.join(os.path.dirname(__file__), "data.sqlite")
    exists = os.path.isfile(database)
    with app.app_context():
        db.create_all()
        if not exists:
            from models.user import User
            from hashlib import sha256
            from bcrypt import gensalt, hashpw

            db.session.add(
                User(
                    id="admin",
                    name="admin",
                    password=hashpw(sha256(b"admin").hexdigest().encode(), gensalt()),
                    admin=True,
                ),
            )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
