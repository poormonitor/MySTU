from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import re

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
@jwt_required()
def search():
    from models.student import Student
    from models import db
    from const import info

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

    result = result.limit(5)
    result = result.all()

    def getContent(student: Student, keyword: str):
        s, f = "", ""
        for key, value in student.to_dict().items():
            s += info[key] + ": " + str(value)
            s += "\n"

        for target in keyword.split(" "):
            rs = re.search(r".*(%s).+" % target, s)

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
    print(result)

    return jsonify(status="ok", data=result)
