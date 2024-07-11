from server import app
import pandas as pd
import sys
import os
import json

if len(sys.argv) < 2:
    filename = input("请输入文件路径：")
    delete = False
else:
    filename = sys.argv[1]
    delete = True

df = pd.read_excel(filename, dtype="str", engine="openpyxl")

typ = 0

if "不及格学分" in df.columns:
    typ = 0
    default = "[0,0,0]"
elif "课程名称" in df.columns:
    typ = 1
    default = "[]"
elif "学时" in df.columns:
    typ = 2
    default = "[]"
elif "奖惩原因" in df.columns:
    typ = 3
    default = "[]"
else:
    raise ValueError("Unknown type of data")

with app.app_context():
    from models.record import Record
    from models import db

    match typ:
        case 0:
            Record.query.update({"score": default})
            db.session.commit()

            for i in df.to_dict(orient="records"):
                id = i.get("学号", "")
                cols = ["不及格学分", "获得学分", "平均学分绩点"]
                detail = [i.get(j, "") for j in cols]
                content = json.dumps(detail)

                record = Record.query.filter_by(id=id).first()
                if not record:
                    record = Record(id=id)
                    db.session.add(record)

                record.score = content
                record.last_update = db.func.now()
                db.session.commit()

        case 1 | 2 | 3:
            cols = {
                1: ["课程名称", "学分", "成绩", "课程性质"],
                2: ["时间", "内容", "学时"],
                3: ["奖惩原因", "奖惩级别", "奖惩时间"],
            }

            attr = {
                1: "unqualified",
                2: "attendance",
                3: "award",
            }

            Record.query.update({attr[typ]: default})
            db.session.commit()

            cols = cols[typ]
            attr = attr[typ]

            ids = df["学号"].unique()
            for id in ids:
                records = df[df["学号"] == id].to_dict(orient="records")
                detail = [[i.get(j, "") for j in cols] for i in records]
                content = json.dumps(detail)

                record = Record.query.filter_by(id=id).first()
                if not record:
                    record = Record(id=id)
                    db.session.add(record)

                setattr(record, attr, content)
                record.last_update = db.func.now()
                db.session.commit()


if delete:
    os.remove(filename)
