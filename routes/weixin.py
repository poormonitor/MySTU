import base64
import datetime
import json
from urllib.parse import unquote

import jwt
import requests
from flask import Blueprint, current_app, jsonify, redirect, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

weixin_bp = Blueprint("weixin", __name__)


@weixin_bp.route("/wx/appid", methods=["GET"])
def weixin_appid():
    return jsonify(status="ok", data={"appid": current_app.config["WEIXIN_APPID"]})


@weixin_bp.route("/wx/info", methods=["GET"])
@jwt_required()
def weixin_info():
    from models.student import Student

    sid = get_jwt_identity()
    payload = get_jwt()

    if not (payload.get("weixin", False) and payload.get("type", 0) == 1):
        return jsonify(status="error", message="Permission denied")

    student = Student.query.filter_by(id=sid).first()
    if not student:
        return jsonify(status="error", message="Student not found")

    data = {"name": student.name, "class": student.cls, "id": student.id}

    return jsonify(status="ok", data=data)


@weixin_bp.route("/wx/login", methods=["GET"])
def weixin_login():
    from datetime import datetime, timezone

    from models import db
    from models.user import User
    from models.weixin import Weixin

    code = request.args.get("code")
    if not code:
        return redirect(f"/#/wx/error?error=2")

    appid = current_app.config["WEIXIN_APPID"]
    secret = current_app.config["WEIXIN_APPSECRET"]

    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
    res = requests.get(url)
    res = res.json()
    openid = res.get("openid")

    if not openid:
        return redirect(f"/#/wx/error?error=3")

    weixin = Weixin.query.filter_by(openid=openid).first()
    if not weixin:
        return redirect(f"/#/wx/error?error=1")

    weixin.last_login = datetime.now(timezone.utc)
    db.session.commit()

    if weixin.role == 0:
        user_id = weixin.attach
        user = User.query.filter_by(id=user_id).first()

        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        access_token = create_access_token(
            fresh=True, identity=user.id, additional_claims={"weixin": True, "type": 0}
        )

        role = 0
    else:
        access_token = create_access_token(
            identity=weixin.attach, additional_claims={"weixin": True, "type": 1}
        )

        role = 1

    return redirect(f"/#/wx/welcome?token={access_token}&role={role}")


@weixin_bp.route("/wx/create", methods=["GET"])
@jwt_required(fresh=True)
def weixin_create():
    from models.weixin import Weixin

    attach = request.args.get("attach")
    role = int(request.args.get("role"))

    weixin = Weixin.query.filter_by(attach=attach, role=role).all()
    attached = [[i.nick, i.openid] for i in weixin] if weixin else []

    if role == 0:
        exp = datetime.datetime.now() + datetime.timedelta(minutes=5)
        current = get_jwt_identity()
        if attach != current:
            return jsonify(status="error", message="Permission denied")

        from models.user import User

        user = User.query.filter_by(id=attach).first()
        if not user:
            return jsonify(status="error", message="User not found")

    elif role == 1:
        exp = datetime.datetime.now() + datetime.timedelta(days=1)

        from models.student import Student

        student = Student.query.filter_by(id=attach).first()
        if not student:
            return jsonify(status="error", message="Student not found")

    exp = exp.timestamp()
    exp = int(exp)

    token = jwt.encode(
        {"attach": attach, "role": role, "exp": exp},
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    token = ".".join(token.split(".")[1:])

    return jsonify(status="ok", data={"token": token, "attached": attached})


@weixin_bp.route("/wx/bind", methods=["GET"])
def weixin_bind():
    from models import db
    from models.weixin import Weixin

    try:
        token = unquote(request.args.get("state"))
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        token = header + "." + token
        claims = jwt.decode(
            token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return redirect(f"/#/wx/error?error=4")
    except:
        return redirect(f"/#/wx/error?error=2")

    code = request.args.get("code")
    if not code:
        return redirect(f"/#/wx/error?error=2")

    attach = claims.get("attach")
    role = int(claims.get("role"))

    weixin = Weixin.query.filter_by(attach=attach, role=role).count()
    if role == 0 and weixin >= 1:
        return redirect(f"/#/wx/error?error=7")
    if role == 1 and weixin >= 2:
        return redirect(f"/#/wx/error?error=7")

    appid = current_app.config["WEIXIN_APPID"]
    secret = current_app.config["WEIXIN_APPSECRET"]

    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
    res = requests.get(url)
    res = res.json()
    openid = res.get("openid", None)
    access_token = res.get("access_token", None)

    weixin = Weixin.query.filter_by(openid=openid).first()
    if weixin:
        return redirect(f"/#/wx/error?error=8")

    url = f"https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
    res = requests.get(url)
    res = res.json()
    nickname = res.get("nickname", None)
    nickname = nickname.encode("iso-8859-1").decode("utf-8")

    if not openid:
        return redirect(f"/#/wx/error?error=3")

    weixin = Weixin(openid=openid, role=role, attach=attach, nick=nickname)
    db.session.add(weixin)
    db.session.commit()

    return redirect(f"/#/wx/welcome")


@weixin_bp.route("/wx/unbind", methods=["POST"])
@jwt_required()
def weixin_unbind():
    from models import db
    from models.weixin import Weixin

    openid = request.json.get("openid")
    weixin = Weixin.query.filter_by(openid=openid).first()
    if not weixin:
        return jsonify(status="error", message="Weixin not found")

    db.session.delete(weixin)
    db.session.commit()

    return jsonify(status="ok", data={})


@weixin_bp.route("/wx/add", methods=["GET"])
def weixin_add():
    from models import db
    from models.student import Student
    from models.weixin import Weixin

    try:
        token = unquote(request.args.get("state"))
        claims = json.loads(base64.b64decode(token).decode())
    except:
        return redirect(f"/#/wx/error?error=2")

    code = request.args.get("code")
    if not code:
        return redirect(f"/#/wx/error?error=2")

    sid = claims.get("sid")
    phone = claims.get("phone")
    attach = sid
    role = 1

    weixin = Weixin.query.filter_by(attach=attach, role=role).first()
    if weixin:
        return redirect(f"/#/wx/error?error=7")

    student = Student.query.filter_by(id=sid).first()
    if not student:
        return redirect(f"/#/wx/error?error=5")

    if phone != student.fcontact1phone and phone != student.fcontact2phone:
        return redirect(f"/#/wx/error?error=6")

    appid = current_app.config["WEIXIN_APPID"]
    secret = current_app.config["WEIXIN_APPSECRET"]

    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
    res = requests.get(url)
    res = res.json()
    openid = res.get("openid", None)
    access_token = res.get("access_token", None)

    weixin = Weixin.query.filter_by(openid=openid).count()
    if weixin >= 2:
        return redirect(f"/#/wx/error?error=8")

    if not openid:
        return redirect(f"/#/wx/error?error=3")

    url = f"https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
    res = requests.get(url)
    res = res.json()
    nickname = res.get("nickname", None)
    nickname = nickname.encode("iso-8859-1").decode("utf-8")

    weixin = Weixin(openid=openid, role=role, attach=attach, nick=nickname)
    db.session.add(weixin)
    db.session.commit()

    return redirect(f"/#/wx/welcome")
