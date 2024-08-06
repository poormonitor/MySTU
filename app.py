# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 10:07
# @Author  : Johnson Sun (@poormonitor)
# @Email   : poormonitor@outlook.com
# @File    : app.py

import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models import init_app as models_init_app
from routes import init_app as routes_init_app


def create_app():
    app = Flask(__name__)

    CORS(app)
    JWTManager(app)

    config = os.getenv("CONFIG", "config.Config")
    app.config.from_object(config)

    db = models_init_app(app)
    routes_init_app(app)

    with app.app_context():
        db.create_all()

        from models.user import User

        user = db.session.query(User).filter_by(admin=True).count()
        if not user:
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
