import os
import sys

import pandas as pd

from const import info
from server import app

if len(sys.argv) < 2:
    filename = input("请输入文件路径：")
    delete = False
else:
    filename = sys.argv[1]
    delete = True

df = pd.read_excel(filename, dtype="str", engine="openpyxl")
df.columns = df.columns.map(lambda x: x.replace("*", ""))
df = df.drop_duplicates(subset=["学号"])
df = df.applymap(lambda x: x if str(x) != "nan" else "")
df = df.applymap(lambda x: x.replace(" ", "") if isinstance(x, str) else x)
df["居住地"] = df["居住地"].apply(lambda x: x.replace(",", ""))
df["性别"] = df["性别"].apply(lambda x: 0 if x == "男" else 1)

with app.app_context():
    from models import db
    from models.student import Student

    for i in df.to_dict(orient="records"):
        detail = [i.get(j, "") for j in info.values()]
        id = detail[0]

        if Student.query.filter_by(id=id).first():
            stu = Student.query.filter_by(id=id)
            stu.update({k: v for k, v in zip(info.values(), detail)})
        else:
            db.session.add(Student(*detail))

        db.session.commit()

if delete:
    os.remove(filename)
