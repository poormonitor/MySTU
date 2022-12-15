from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bcrypt import checkpw, gensalt, hashpw
from models.user import User
from models import db

manage_bp = Blueprint("manage", __name__)


@manage_bp.route("/passwd", methods=["POST"])
@jwt_required()
def passwd():
    old = request.json.get("old", None)
    new = request.json.get("new", None)

    correct = User.query.filter_by(id=get_jwt_identity()).first()

    if not checkpw(old.encode(), correct.passwd):
        return jsonify(status="error")

    correct.passwd = hashpw(new.encode(), gensalt())
    db.session.commit()

    return jsonify(status="ok")
