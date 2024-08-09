from datetime import datetime, timezone

from bcrypt import checkpw
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from models import db
from models.user import User

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    uid = request.json.get("user", None)
    passwd = request.json.get("passwd", None)

    result = User.query.filter_by(id=uid).first()

    if not result:
        return jsonify(
            status="error",
            data={"msg": "您输入的用户不存在，请检查"},
        )

    if not checkpw(passwd.encode(), result.passwd.encode()):
        return jsonify(
            status="error",
            data={"msg": "您输入的密码不正确，请检查"},
        )

    result.last_login = datetime.now(timezone.utc)
    db.session.commit()

    access_token = create_access_token(
        identity=uid,
        additional_claims={"admin": result.admin, "name": result.name},
        fresh=True,
    )

    return jsonify(
        status="ok",
        data={"access_token": access_token, "name": result.name, "admin": result.admin},
    )
