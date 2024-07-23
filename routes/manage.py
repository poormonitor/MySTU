from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from models.user import User
from models.weixin import Weixin
from models import db

manage_bp = Blueprint("manage", __name__)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        claims = get_jwt()
        if not claims["admin"]:
            return jsonify(status="error")
        else:
            return f(*args, **kwargs)

    return wrap


@manage_bp.route("/passwd", methods=["POST"])
@jwt_required(fresh=True)
def passwd():
    from bcrypt import checkpw, gensalt, hashpw

    old = request.json.get("old", None)
    new = request.json.get("new", None)

    correct = User.query.filter_by(id=get_jwt_identity()).first()

    if not checkpw(old.encode(), correct.passwd):
        return jsonify(status="error")

    correct.passwd = hashpw(new.encode(), gensalt())
    db.session.commit()

    return jsonify(status="ok")


@manage_bp.route("/admin/user")
@jwt_required(fresh=True)
@admin_required
def getUsers():
    from const import datetime_to_str

    users = [i.to_dict() for i in User.query.all()]
    for i in range(len(users)):
        last_login = datetime_to_str(d) if (d := users[i]["last_login"]) else ""
        users[i]["last_login"] = last_login

        weixin = Weixin.query.filter_by(attach=users[i]["id"], role=0).first()
        users[i]["weixin"] = [weixin.nick, weixin.openid] if weixin else None

        del users[i]["passwd"]

    return jsonify(status="ok", data={"users": users})


@manage_bp.route("/admin/admin", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def switchAdmin():
    data = request.get_json()
    uid, val = data["id"], bool(data["val"])

    user = User.query.filter_by(id=uid).first()
    user.admin = val
    db.session.commit()

    return jsonify(status="ok")


@manage_bp.route("/admin/passwd", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def editPasswd():
    from bcrypt import gensalt, hashpw

    data = request.get_json()
    uid, passwd = data["user"], data["passwd"]

    user = User.query.filter_by(id=uid).first()
    user.passwd = hashpw(passwd.encode(), gensalt())
    db.session.commit()

    return jsonify(status="ok")


@manage_bp.route("/admin/new", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def newUser():
    from bcrypt import gensalt, hashpw

    data = request.get_json()
    uid, passwd, name, admin = data["id"], data["passwd"], data["user"], data["admin"]
    passwd = hashpw(passwd.encode(), gensalt())

    user = User.query.filter_by(id=uid).first()
    if user:
        return jsonify(status="error", data={"msg": "已经有相同用户名用户存在"})

    db.session.add(User(uid, name, passwd, admin))
    db.session.commit()

    return jsonify(status="ok")


@manage_bp.route("/admin/download", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def download():
    from models import db
    from models.student import Student
    from models.weixin import Weixin
    from const import info

    import base64
    from io import BytesIO
    import pandas as pd
    import html2text

    cls = request.get_json()["cls"]

    WeixinS = db.session.query(Weixin).filter(Weixin.role == 1).subquery()
    WeixinA = db.aliased(Weixin, WeixinS)

    students = db.session.query(Student, WeixinA).select_from(Student)
    students = students.join(WeixinA, WeixinA.attach == Student.id, isouter=True)

    if cls:
        students = students.filter(Student.cls == cls)

    students = students.order_by(Student.cls.asc(), Student.id.asc()).all()

    data = {}
    for i in students:
        for key in info:
            data.setdefault(info[key], []).append(getattr(i[0], key))
        data.setdefault("微信绑定", []).append(i[1].nick if i[1] else "")
    
    data["备注"] = map(html2text.html2text, data["备注"])

    df = pd.DataFrame(data)

    buffer = BytesIO()
    writer = pd.ExcelWriter(buffer, engine="openpyxl")
    df.to_excel(excel_writer=writer, index=False, sheet_name="学生信息")
    writer.close()
    excel_content = buffer.getvalue()
    base64_content = base64.b64encode(excel_content).decode("utf-8")

    return jsonify(status="ok", data={"file": base64_content})


@manage_bp.route("/admin/delete", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def deleteUser():
    data = request.get_json()
    uid = data["id"]

    user = User.query.filter_by(id=uid).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify(status="ok")


@manage_bp.route("/admin/upload", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def upload():
    from tempfile import NamedTemporaryFile
    import subprocess
    import sys
    import os

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    data = request.files["data"]
    filename = NamedTemporaryFile(delete=False, suffix=".xlsx").name
    data.save(filename)
    subprocess.Popen([sys.executable, os.path.join(path, "import.py"), filename])

    return jsonify(status="ok")


@manage_bp.route("/admin/upload_record", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def upload_record():
    from tempfile import NamedTemporaryFile
    import subprocess
    import sys
    import os

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    data = request.files["data"]
    filename = NamedTemporaryFile(delete=False, suffix=".xlsx").name
    data.save(filename)
    subprocess.Popen([sys.executable, os.path.join(path, "import_record.py"), filename])

    return jsonify(status="ok")


@manage_bp.route("/admin/image", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def image():
    import os

    data = request.files["data"]
    filename = data.filename

    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    if not os.path.exists("uploads/pic"):
        os.mkdir("uploads/pic")
    if os.path.exists("uploads/pic/" + filename):
        os.remove("uploads/pic/" + filename)

    data.save("uploads/pic/" + filename)

    return jsonify(status="ok")


@manage_bp.route("/admin/delete/class", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def delete_class():
    from models.student import Student
    import os

    data = request.get_json()
    cls = data["cls"]

    clsList = db.session.query(Student.cls).distinct().order_by(Student.cls.asc()).all()
    clsName = clsList[cls][0]

    ids = [i.id for i in Student.query.filter_by(cls=clsName).all()]

    for i in ids:
        if os.path.exists("uploads/pic/" + i + ".*"):
            os.remove("uploads/pic/" + i + ".*")

    Student.query.filter_by(cls=clsName).delete()
    db.session.commit()

    return jsonify(status="ok")


@manage_bp.route("/admin/delete/student", methods=["POST"])
@jwt_required(fresh=True)
@admin_required
def delete_student():
    from models.student import Student
    import os

    data = request.get_json()
    id = data["id"]

    Student.query.filter_by(id=id).delete()
    db.session.commit()

    if os.path.exists("uploads/pic/" + id + ".*"):
        os.remove("uploads/pic/" + id + ".*")

    return jsonify(status="ok")
