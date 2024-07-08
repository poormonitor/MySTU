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
import base64
import json
import datetime

weixin_bp = Blueprint("weixin", __name__)


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

    if not openid:
        return redirect(f"/#/wx/error?error=3")

    weixin = Weixin.query.filter_by(openid=openid).first()
    if not weixin:
        return redirect(f"/#/wx/error?error=1")

    weixin.last_login = db.func.now()
    db.session.commit()

    if weixin.role == 0:
        user_id = weixin.attach
        user = User.query.filter_by(id=user_id).first()

        user.last_login = db.func.now()
        db.session.commit()

        access_token = create_access_token(
            identity=user.id, additional_claims={"type": 0}
        )

        role = 0
    else:
        access_token = create_access_token(
            identity=weixin.attach, additional_claims={"type": 1}
        )

        role = 1

    return redirect(f"/#/wx/welcome?token={access_token}&role={role}")


@weixin_bp.route("/wx/create", methods=["GET"])
@jwt_required()
def weixin_create():
    from models.weixin import Weixin

    attach = request.args.get("attach")
    role = request.args.get("role")
    timestamp = datetime.datetime.now().timestamp()

    weixin = Weixin.query.filter_by(attach=attach, role=role).first()
    attached = weixin is not None

    if role == 0:
        current = get_jwt_identity()
        if attach != current:
            return jsonify(status="error", message="Permission denied")

        from models.user import User

        user = User.query.filter_by(id=attach).first()
        if not user:
            return jsonify(status="error", message="User not found")

        timestamp = timestamp + 5 * 60

    elif role == 1:
        from models.student import Student

        student = Student.query.filter_by(id=attach).first()
        if not student:
            return jsonify(status="error", message="Student not found")

        timestamp = timestamp + 24 * 60 * 60

    timestamp = int(timestamp)

    token = jwt.encode(
        {"attach": attach, "role": role, "exp": timestamp},
        Config.JWT_SECRET_KEY,
        algorithm="HS256",
    )

    token = ".".join(token.split(".")[1:])

    return jsonify(status="ok", data={"token": token, "attached": attached})


@weixin_bp.route("/wx/bind", methods=["GET"])
def weixin_bind():
    from models.weixin import Weixin
    from models import db

    try:
        token = unquote(request.args.get("state"))
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        token = header + "." + token
        print(token)
        claims = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return redirect(f"/#/wx/error?error=4")
    except:
        return redirect(f"/#/wx/error?error=2")

    code = request.args.get("code")
    if not code:
        return redirect(f"/#/wx/error?error=2")

    attach = claims.get("attach")
    role = claims.get("role")

    weixin = Weixin.query.filter_by(attach=attach, role=role).first()
    if weixin:
        return redirect(f"/#/wx/error?error=7")

    weixin = Weixin.query.filter_by(openid=openid).first()
    if weixin:
        return redirect(f"/#/wx/error?error=8")

    appid = Config.WEIXIN_APPID
    secret = Config.WEIXIN_APPSECRET

    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
    res = requests.get(url)
    res = res.json()
    openid = res.get("openid", None)
    access_token = res.get("access_token", None)

    url = f"https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
    res = requests.get(url)
    res = res.json()
    nickname = res.get("nickname", None)

    if not openid:
        return redirect(f"/#/wx/error?error=3")

    weixin = Weixin(openid=openid, role=role, attach=attach, nick=nickname)
    db.session.add(weixin)
    db.session.commit()

    return redirect(f"/#/wx/welcome")


@weixin_bp.route("/wx/unbind", methods=["GET"])
@jwt_required()
def weixin_unbind():
    from models.weixin import Weixin
    from models import db

    attach = request.args.get("attach")
    role = request.args.get("role")
    weixin = Weixin.query.filter_by(attach=attach, role=role).first()
    if not weixin:
        return jsonify(status="error", message="Weixin not found")

    db.session.delete(weixin)
    db.session.commit()

    return jsonify(status="ok", data={})


@weixin_bp.route("/wx/add", methods=["GET"])
def weixin_add():
    from models.student import Student
    from models.weixin import Weixin
    from models import db

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

    student = Student.query.filter_by(sid=sid).first()
    if not student:
        return redirect(f"/#/wx/error?error=5")

    if phone != student.fcontact1phone or phone != student.fcontact2phone:
        return redirect(f"/#/wx/error?error=6")

    appid = Config.WEIXIN_APPID
    secret = Config.WEIXIN_APPSECRET

    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
    res = requests.get(url)
    res = res.json()
    openid = res.get("openid", None)
    access_token = res.get("access_token", None)

    if not openid:
        return redirect(f"/#/wx/error?error=3")

    url = f"https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
    res = requests.get(url)
    res = res.json()
    nickname = res.get("nickname", None)

    weixin = Weixin(openid=openid, role=role, attach=attach, nick=nickname)
    db.session.add(weixin)
    db.session.commit()

    return redirect(f"/#/wx/welcome")
