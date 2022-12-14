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
