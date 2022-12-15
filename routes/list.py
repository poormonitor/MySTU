from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

list_bp = Blueprint("list", __name__)


@list_bp.route("/classes")
@jwt_required()
def getClasses():
    from models.student import Student
    from models import db

    clsList = db.session.query(Student.cls).distinct().order_by(Student.cls.asc()).all()
    clsList = [{"id": i, "name": clsList[i][0]} for i in range(len(clsList))]

    return jsonify(status="ok", data={"clsList": clsList})


@list_bp.route("/students")
@jwt_required()
def getStudents():
    from models.student import Student
    from models import db

    cls = request.args.get("class")
    clsName = (
        db.session.query(Student.cls)
        .distinct()
        .order_by(Student.cls.asc())
        .all()[int(cls)][0]
    )
    stuList = (
        db.session.query(Student.id, Student.name)
        .filter(Student.cls == clsName)
        .order_by(Student.name.asc())
        .all()
    )
    stuList = [{"id": i[0], "name": i[1]} for i in stuList]

    return jsonify(status="ok", data={"stuList": stuList})


@list_bp.route("/student")
@jwt_required()
def getStudentInfo():
    from models.student import Student

    sid = request.args.get("student")
    student = Student.query.filter_by(id=sid).first().to_dict()
    student["sex"] = ["男", "女"][student["sex"]]

    return jsonify(status="ok", data={"studentInfo": student})


@list_bp.route("/logs")
@jwt_required()
def getLogs():
    from models.log import Log
    from models import db

    student = request.args.get("student")

    logs = (
        db.session.query(Log.id, Log.indate, Log.user, Log.title)
        .filter_by(student=student)
        .order_by(Log.indate.desc())
        .all()
    )

    logs = [
        {
            "id": i[0],
            "time": i[1].strftime("%Y-%m-%d %H:%M:%S"),
            "user": i[2],
            "title": i[3],
        }
        for i in logs
    ]

    return jsonify(status="ok", data={"logList": logs})


@list_bp.route("/record")
@jwt_required()
def getLog():
    from models.log import Log

    logid = request.args.get("id")

    logInfo = Log.query.filter_by(id=logid).first()
    logInfo = logInfo.to_dict()
    logInfo["indate"] = logInfo["indate"].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(status="ok", data={"logInfo": logInfo})
