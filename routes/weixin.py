from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
import jwt
import requests
from config import Config
from urllib.parse import unquote
import hashlib
import base64

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


@weixin_bp.route("/wx/login", methods=["GET"])
def weixin_login():
    from models.weixin import Weixin
    from models.user import User
    from models import db

    code = request.args.get("code")
    if not code:
        return redirect(f"/#/wx/error?error=2")

    appid = Config.WEIXIN_APPID
    secret = Config.WEIXIN_APPSECRET

    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
    res = requests.get(url)
    res = res.json()
    openid = res.get("openid")

    weixin = Weixin.query.filter_by(openid=openid).first()
    if not weixin:
        return redirect(f"/#/wx/error?error=1")

    if weixin.role == 0:
        user_id = weixin.attach
        user = User.query.filter_by(openid=user_id).first()

        user.last_login = db.func.now()
        db.session.commit()

        access_token = create_access_token(
            identity=user.id, additional_claims={"type": 0}
        )

        role = 0
    else:
        access_token = create_access_token(
            identity=openid, additional_claims={"type": 1, "attach": weixin.attach}
        )

        role = 1

    return redirect(f"/#/wx/welcome?token={access_token}&role={role}")


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

        user = User.query.filter_by(id=attach).first()
        if not user:
            return jsonify(status="error", message="User not found")
    elif role == 1:
        from models.student import Student

        student = Student.query.filter_by(id=attach).first()
        if not student:
            return jsonify(status="error", message="Student not found")

    print(Config.JWT_SECRET_KEY, {"attach": attach, "role": role})
    token = jwt.encode(
        {"attach": attach, "role": role},
        Config.JWT_SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify(status="ok", data={"token": token})


@weixin_bp.route("/wx/bind", methods=["GET"])
def weixin_bind():
    from models.weixin import Weixin
    from models import db

    try:
        token = unquote(request.args.get("state"))
        claims = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        print(e)
        return redirect(f"/#/wx/error?error=2")

    code = request.args.get("code")
    if not code:
        return redirect(f"/#/wx/error?error=2")

    appid = Config.WEIXIN_APPID
    secret = Config.WEIXIN_APPSECRET

    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
    res = requests.get(url)
    res = res.json()
    openid = res.get("openid", None)

    if not openid:
        return redirect(f"/#/wx/error?error=3")

    attach = claims.get("attach")
    role = claims.get("role")

    Weixin.query.filter_by(openid=openid).delete()
    Weixin.query.filter_by(attach=attach).delete()

    weixin = Weixin(openid=openid, role=role, attach=attach)
    db.session.add(weixin)
    db.session.commit()

    return redirect(f"/#/wx/welcome")
