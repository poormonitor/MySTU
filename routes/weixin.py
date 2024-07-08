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
import datetime
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply

weixin_bp = Blueprint("weixin", __name__)


def weixin_verify():
    try:
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")
        token = Config.WEIXIN_TOKEN

        check_signature(token, signature, timestamp, nonce)
        return echostr
    except InvalidSignatureException:
        return "Invalid signature"


def weixin_message():
    xml = request.data
    msg = parse_message(xml)
    openid = msg.source
    msgtype = msg.type

    if msgtype == "text":
        content = msg.content
        content = content.split(" ")

        if content[0] == "绑定":
            sid = content[1]
            phone = content[2]

            from models.student import Student

            student = Student.query.filter_by(sid=sid).first()
            if not student:
                reply = TextReply(content="学号不存在", message=msg)
                return reply.render()

            if phone != student.fcontact1phone or phone != student.fcontact2phone:
                reply = TextReply(content="手机号错误", message=msg)
                return reply.render()

            from models.weixin import Weixin
            from models import db

            Weixin.query.filter_by(openid=openid).delete()
            Weixin.query.filter_by(attach=student.id).delete()

            weixin = Weixin(openid=openid, role=1, attach=student.id)
            db.session.add(weixin)
            db.session.commit()

            content = "绑定成功"
            reply = TextReply(content=content, message=msg)
            return reply.render()

        return "success"


@weixin_bp.route("/wx", methods=["GET", "POST"])
def weixin_index():
    if request.method == "GET":
        return weixin_verify()
    else:
        return weixin_message()


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

    token = jwt.encode(
        {"attach": attach, "role": role, "exp": timestamp},
        Config.JWT_SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify(status="ok", data={"token": token, "attached": attached})


@weixin_bp.route("/wx/bind", methods=["GET"])
def weixin_bind():
    from models.weixin import Weixin
    from models import db

    try:
        token = unquote(request.args.get("state"))
        claims = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    except:
        return redirect(f"/#/wx/error?error=2")

    timestamp = claims.get("exp")
    if timestamp < datetime.datetime.now().timestamp():
        return redirect(f"/#/wx/error?error=4")

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
