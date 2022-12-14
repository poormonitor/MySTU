from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from models.user import User
from bcrypt import checkpw

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    uid = request.json.get("user", None)
    passwd = request.json.get("passwd", None)

    result = User.query.filter_by(id=uid).first()
    if not result:
        return jsonify(
            status="error",
            error={"text": "您输入的用户不存在，请检查。", "icon": "error", "title": "用户不存在"},
        )
    if not checkpw(passwd.encode(), result.passwd):
        return jsonify(
            status="error",
            error={"text": "您输入的密码不正确，请检查。", "icon": "error", "title": "密码错误"},
        )

    access_token = create_access_token(identity=uid)
    return jsonify(status="ok", data={"access_token": access_token})
