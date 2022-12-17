from server import app
import pandas as pd
import sys

if len(sys.argv) < 2:
    filename = input("请输入文件路径：")
    delete = False
else:
    filename = sys.argv[1]
    delete = True

df = pd.read_excel(filename, dtype="str")
df.columns = df.columns.map(lambda x: x.replace("*", ""))
df = df.drop("当前位置", axis=1)
df = df.drop("邮编", axis=1)
df = df.drop("序号", axis=1)
df = df.drop_duplicates(subset=["学号"])
df = df.applymap(lambda x: x if str(x) != "nan" else "")
df = df.applymap(lambda x: x.replace(" ", "") if isinstance(x, str) else x)
df["居住地"] = df["居住地"].apply(lambda x: x.replace(",", ""))
df["性别"] = df["性别"].apply(lambda x: 0 if x == "男" else 1)

with app.app_context():
    from models.student import Student
    from models import db

    for i in list(df.to_numpy()):
        db.session.add(Student(*list(i)))
        db.session.commit()

if delete:
    os.remove(filename)
