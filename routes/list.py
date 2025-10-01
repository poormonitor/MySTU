from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from const import datetime_to_str

list_bp = Blueprint("list", __name__)


@list_bp.route("/classes")
@jwt_required(fresh=True)
def getClasses():
    from datetime import datetime, timedelta, timezone

    from models import db
    from models.log import Log
    from models.student import Student

    clsList = db.session.query(Student.cls).distinct().order_by(Student.cls.asc()).all()

    date_after = datetime.now(timezone.utc) - timedelta(days=7)

    logCnt = db.session.query(Student.cls, db.func.count(Log.id))
    logCnt = logCnt.outerjoin(Student, Student.id == Log.student)
    logCnt = logCnt.group_by(Student.cls)
    logCnt = logCnt.filter(Log.indate >= date_after)
    logCnt = logCnt.all()

    memoCnt = db.session.query(Student.cls.distinct())
    memoCnt = memoCnt.filter(Student.memoupdate >= date_after)
    memoCnt = memoCnt.all()

    logCnt = {i[0] for i in logCnt if i[1] > 0}
    memoCnt = {i[0] for i in memoCnt}
    logCnt = logCnt.union(memoCnt)

    clsList = [
        {
            "id": i,
            "name": clsList[i][0],
            "alert": clsList[i][0] in logCnt,
        }
        for i in range(len(clsList))
    ]

    return jsonify(status="ok", data={"clsList": clsList})


@list_bp.route("/students")
@jwt_required(fresh=True)
def getStudents():
    from datetime import datetime, timedelta

    from models import db
    from models.log import Log
    from models.student import Student
    from models.weixin import Weixin

    cls = request.args.get("class")
    clsName = db.session.query(Student.cls)
    clsName = clsName.distinct()
    clsName = clsName.order_by(Student.cls.asc())
    clsName = clsName.all()[int(cls)][0]

    stuList = db.session.query(Student.id, Student.name)
    stuList = stuList.filter(Student.cls == clsName)
    stuList = stuList.order_by(Student.name.asc())
    stuList = stuList.all()

    logCnt = db.session.query(Student.id, db.func.count(Log.id))
    logCnt = logCnt.outerjoin(Student, Student.id == Log.student)
    logCnt = logCnt.group_by(Student.id)
    logCnt = logCnt.filter(Student.cls == clsName)
    logCnt = logCnt.filter(Log.indate >= datetime.now() - timedelta(days=7))
    logCnt = logCnt.all()

    memoCnt = db.session.query(Student.id)
    memoCnt = memoCnt.filter(Student.cls == clsName)
    memoCnt = memoCnt.filter(Student.memoupdate >= datetime.now() - timedelta(days=7))
    memoCnt = memoCnt.all()

    logCnt = {i[0] for i in logCnt if i[1] > 0}
    memoCnt = {i[0] for i in memoCnt}
    logCnt = logCnt.union(memoCnt)

    subquery = db.session.query(Student.id).filter(Student.cls == clsName).subquery()
    weixinAttached = db.session.query(subquery)
    weixinAttached = weixinAttached.join(Weixin, Weixin.attach == subquery.c.id)

    stuList = [
        {
            "id": i[0],
            "name": i[1],
            "alert": i[0] in logCnt,
            "weixin": i[0] in weixinAttached,
        }
        for i in stuList
    ]

    return jsonify(status="ok", data={"stuList": stuList})


@list_bp.route("/student")
@jwt_required(fresh=True)
def getStudentInfo():
    from models.student import Student
    from models.weixin import Weixin

    sid = request.args.get("student")
    student = Student.query.filter_by(id=sid).first().to_dict()

    if not student:
        return jsonify(status="error", message="学生不存在")

    student["sex"] = ["男", "女"][student["sex"]]

    weixin = Weixin.query.filter_by(attach=sid).first()
    student["attached"] = weixin is not None

    return jsonify(status="ok", data={"studentInfo": student})


@list_bp.route("/record")
@jwt_required()
def getStudentRecord():
    import json

    from models.record import Record

    sid = request.args.get("student")

    payload = get_jwt()
    if payload.get("weixin", True) and payload.get("type", 1) == 1:
        current = get_jwt_identity()
        if sid != current:
            return jsonify(status="error", message="Permission denied")

    record = Record.query.filter_by(id=sid).first()

    empty = {
        "score": [],
        "unqualified": [],
        "attendance": [],
        "award": [],
        "warning": [],
        "activity": [],
    }

    if not record:
        data = empty
    else:
        data = {i: json.loads(j) for i, j in record.to_dict().items() if i in empty}

    data["last_update"] = datetime_to_str(record.last_update) if record else "未知"

    return jsonify(status="ok", data={"studentRecord": data})


@list_bp.route("/logs")
@jwt_required(fresh=True)
def getLogs():
    from const import datetime_to_str
    from models import db
    from models.log import Log
    from models.user import User

    student = request.args.get("student")

    logs = db.session.query(Log.id, Log.indate, User.name, Log.title)
    logs = logs.outerjoin(User, User.id == Log.user)
    logs = logs.filter(Log.student == student)
    logs = logs.order_by(Log.indate.desc())
    logs = logs.all()

    logs = [
        {
            "id": i[0],
            "time": datetime_to_str(i[1]),
            "user": i[2],
            "title": i[3],
        }
        for i in logs
    ]

    return jsonify(status="ok", data={"logList": logs})


@list_bp.route("/log")
@jwt_required(fresh=True)
def getLog():
    from const import datetime_to_str
    from models.log import Log

    logid = request.args.get("log")

    logInfo = Log.query.filter_by(id=logid).first()

    if not logInfo:
        return jsonify(status="error", message="记录不存在")

    logInfo = logInfo.to_dict()
    logInfo["indate"] = datetime_to_str(logInfo["indate"])

    return jsonify(status="ok", data={"logInfo": logInfo})


@list_bp.route("/pic")
@jwt_required(fresh=True)
def getPic():
    from base64 import b64encode

    sid = request.args.get("id")
    try:
        with open("uploads/pic/" + sid + ".jpg", "rb") as fp:
            content = fp.read()
    except FileNotFoundError:
        return jsonify(status="error")

    resp = make_response(
        jsonify(
            status="ok", data={"format": "jpeg", "pic": b64encode(content).decode()}
        )
    )

    resp.headers["Cache-Control"] = "private, max-age=604800"

    return resp
