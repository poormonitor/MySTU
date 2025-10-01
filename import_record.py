import json
import os
import sys

import pandas as pd

from server import app

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
    default = "[]"
elif "课程名称" in df.columns:
    typ = 1
    default = "[]"
elif "学时" in df.columns:
    typ = 2
    default = "[]"
elif "奖惩原因" in df.columns:
    typ = 3
    default = "[]"
elif "提醒" in df.columns:
    typ = 4
    default = "[]"
elif "活动名称" in df.columns:
    typ = 5
    default = "[]"
else:
    raise ValueError("Unknown type of data")

with app.app_context():
    from datetime import datetime, timezone

    from models import db
    from models.record import Record

    match typ:
        case 0:
            Record.query.update({"score": default})
            db.session.commit()

            for i in df.to_dict(orient="records"):
                id = i.get("学号", "")
                cols = ["不及格学分", "获得学分", "平均学分绩点", "专业排名"]
                detail = [i.get(j, "") for j in cols]
                detail = [j if str(j) != "nan" else "" for j in detail]
                content = json.dumps(detail)

                record = Record.query.filter_by(id=id).first()
                if not record:
                    record = Record(id=id)
                    db.session.add(record)

                record.score = content
                record.last_update = datetime.now(timezone.utc)
                db.session.commit()

        case 1 | 2 | 3 | 4 | 5:
            cols = {
                1: ["课程名称", "学分", "成绩", "课程性质"],
                2: ["时间", "内容", "学时"],
                3: ["奖惩原因", "奖惩级别", "奖惩时间"],
                4: ["提醒"],
                5: ["活动名称", "活动时数", "活动日期"]
            }

            attr = {
                1: "unqualified",
                2: "attendance",
                3: "award",
                4: "warning",
                5: "activity",
            }

            Record.query.update({attr[typ]: default})
            db.session.commit()

            cols = cols[typ]
            attr = attr[typ]

            ids = df["学号"].unique()
            for id in ids:
                records = df[df["学号"] == id].to_dict(orient="records")
                detail = [
                    [i.get(j, "") if str(j) != "nan" else "" for j in cols]
                    for i in records
                ]
                content = json.dumps(detail)

                record = Record.query.filter_by(id=id).first()
                if not record:
                    record = Record(id=id)
                    db.session.add(record)

                setattr(record, attr, content)
                record.last_update = datetime.now(timezone.utc)
                db.session.commit()


if delete:
    os.remove(filename)
