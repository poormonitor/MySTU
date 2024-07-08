from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

submit_bp = Blueprint("submit", __name__)


@submit_bp.route("/submit", methods=["POST"])
@jwt_required(fresh=True)
def submitLog():
    from models.log import Log
    from models import db

    logData = request.get_json()
    logRecord = Log(**logData)
    db.session.add(logRecord)
    db.session.commit()

    return jsonify(status="ok", data={"id": logRecord.id})


@submit_bp.route("/memo", methods=["POST"])
@jwt_required(fresh=True)
def submitMemo():
    from models.student import Student
    from models import db

    memo = request.json.get("memo")
    sid = request.json.get("id")

    student = Student.query.filter_by(id=sid).first()
    student.memo = memo
    db.session.commit()

    return jsonify(status="ok")


@submit_bp.route("/edit", methods=["POST"])
@jwt_required(fresh=True)
def editStudent():
    from models.student import Student
    from models import db

    info = request.get_json()

    student = Student.query.filter_by(id=info["id"]).first()
    for i in info.keys():
        setattr(student, i, info[i])
    db.session.commit()

    return jsonify(status="ok")