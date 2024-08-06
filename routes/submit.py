from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

submit_bp = Blueprint("submit", __name__)


@submit_bp.route("/submit", methods=["POST"])
@jwt_required(fresh=True)
def submitLog():
    from models import db
    from models.log import Log
    from models.student import Student

    student = Student.query.filter_by(id=request.json.get("student")).first()
    if not student:
        return jsonify(status="error", data={"msg": "学生不存在"})

    logData = request.get_json()
    logRecord = Log(**logData)
    db.session.add(logRecord)
    db.session.commit()

    return jsonify(status="ok", data={"id": logRecord.id})


@submit_bp.route("/memo", methods=["POST"])
@jwt_required(fresh=True)
def submitMemo():
    from models import db
    from models.student import Student

    memo = request.json.get("memo")
    sid = request.json.get("id")

    student = Student.query.filter_by(id=sid).first()

    if not student:
        return jsonify(status="error", data={"msg": "学生不存在"})

    student.memo = memo
    db.session.commit()

    return jsonify(status="ok")


@submit_bp.route("/edit", methods=["POST"])
@jwt_required(fresh=True)
def editStudent():
    from models import db
    from models.student import Student

    info = request.get_json()

    student = Student.query.filter_by(id=info["id"]).first()

    if not student:
        return jsonify(status="error", data={"msg": "学生不存在"})

    for i in info.keys():
        setattr(student, i, info[i])
    db.session.commit()

    return jsonify(status="ok")
