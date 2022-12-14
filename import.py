import pandas as pd
from app import create_app

df = pd.read_excel("data.xlsx", dtype="str")

app = create_app()

df.columns = df.columns.map(lambda x: x.replace("*", ""))
df = df.drop("当前位置", axis=1)
df = df.drop("邮编", axis=1)
df = df.drop("序号", axis=1)
df = df.drop_duplicates(subset=["学号"])
df = df.applymap(lambda x: x if str(x) != "nan" else "")
df = df.applymap(lambda x: x.replace(" ", "") if isinstance(x, str) else x)
df["性别"] = df["性别"].apply(lambda x: 0 if x == "男" else 1)

with app.app_context():
    from models.student import Student
    from models import db

    for i in list(df.to_numpy()):
        db.session.add(Student(*list(i)))
        db.session.commit()
