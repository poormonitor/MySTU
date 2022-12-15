from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

submit_bp = Blueprint("submit", __name__)


@submit_bp.route("/submit", methods=["POST"])
@jwt_required()
def submitLog():
    from models.log import Log
    from models import db

    logData = request.get_json()
    logRecord = Log(**logData)
    db.session.add(logRecord)
    db.session.commit()

    return jsonify(status="ok", data={"id": logRecord.id})


@submit_bp.route("/memo", methods=["POST"])
@jwt_required()
def submitMemo():
    from models.student import Student
    from models import db

    memo = request.json.get("memo")
    sid = request.json.get("id")

    student = Student.query.filter_by(id=sid).first()
    student.memo = memo
    db.session.commit()

    return jsonify(status="ok")
