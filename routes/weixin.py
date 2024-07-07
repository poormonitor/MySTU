from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    get_jwt_identity,
)
import jwt
from config import Config
import hashlib

weixin_bp = Blueprint("weixin", __name__)


@weixin_bp.route("/wx")
@jwt_required()
def weixin_index():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")

    if not all([signature, timestamp, nonce]):
        return False

    token = Config.JWT_SECRET_KEY
    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = "".join(tmp_arr)
    tmp_str = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()

    return tmp_str == signature


@weixin_bp.route("/wx/login", methods=["POST"])
@jwt_required()
def weixin_login():
    from models.weixin import Weixin
    from models.user import User
    from models import db

    openid = request.json.get("openid")
    if not openid:
        return "error"

    weixin = Weixin.query.filter_by(openid=openid).first()
    if not weixin:
        return jsonify(status="error", message="User not found")

    if weixin.role == 0:
        user_id = weixin.attach
        user = User.query.filter_by(openid=user_id).first()

        user.last_login = db.func.now()
        db.session.commit()

        access_token = create_access_token(
            identity=user.id, additional_claims={"type": 0}
        )

        return jsonify(
            status="ok",
            data={"access_token": access_token, "type": 0},
        )
    else:
        access_token = create_access_token(
            identity=openid, additional_claims={"type": 1, "attach": weixin.attach}
        )

        return jsonify(status="ok", data={"access_token": access_token, "type": 1})


@weixin_bp.route("/wx/create", methods=["GET"])
@jwt_required()
def weixin_create():
    attach = request.args.get("attach")
    role = request.args.get("role")

    if role == 0:
        current = get_jwt_identity()
        if attach != current:
            return jsonify(status="error", message="Permission denied")

        from models.user import User

        user = User.query.filter_by(openid=attach).first()
        if not user:
            return jsonify(status="error", message="User not found")
    elif role == 1:
        from models.student import Student

        student = Student.query.filter_by(id=attach).first()
        if not student:
            return jsonify(status="error", message="Student not found")

    token = jwt.encode(
        {"attach": attach, "role": role}, Config.JWT_SECRET_KEY, algorithm="HS256"
    )

    return jsonify(status="ok", data={"token": token})


@weixin_bp.route("/wx/bind", methods=["POST"])
def weixin_bind():
    from models.weixin import Weixin
    from models import db

    try:
        token = request.json.get("token")
        claims = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify(status="error", message="Error token")

    openid = request.json.get("openid")
    attach = claims.get("attach")
    role = claims.get("role")

    Weixin.query.filter_by(openid=openid).delete()
    Weixin.query.filter_by(attach=attach).delete()

    weixin = Weixin(openid=openid, role=role, attach=attach)
    db.session.add(weixin)
    db.session.commit()

    return jsonify(status="ok", data={"openid": openid, "attach": attach, "role": role})