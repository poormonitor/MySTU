import re

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
@jwt_required(fresh=True)
def search():
    from const import info
    from models import db
    from models.student import Student

    keyword = request.args.get("s", "")
    ks = keyword.split(" ")

    result = db.session.query(Student).filter(
        db.and_(
            db.or_(
                Student.id.contains(k),
                Student.name.contains(k),
                Student.cls.contains(k),
                Student.domicile.contains(k),
                Student.residence.contains(k),
                Student.domitory.contains(k),
                Student.phone.contains(k),
            )
            for k in ks
        )
    )

    result = result.all()

    def getContent(student: Student, keyword: str):
        s, f = "", ""
        
        for key in info.keys():
            s += info[key] + ": " + str(getattr(student, key))
            s += "\n"

        for target in keyword.split(" "):
            rs = re.search(r".*(%s).*" % target, s)

            if not rs:
                return None

            gp = rs.group(), rs.group(1)
            f += gp[0].replace(gp[1], "<b>" + gp[1] + "</b>") + "\n"

        return {
            "name": student.name,
            "content": f,
            "id": student.id,
            "cls": student.cls,
        }

    result = [e for i in result if (e := getContent(i, keyword))]

    return jsonify(status="ok", data=result)
