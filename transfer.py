from server import app
from models.student import Student
from PIL import Image
from models import db
import os

os.chdir("./uploads/pic/")
with app.app_context():
    for i in os.listdir("./"):
        if "_" in i:
            fname, fmat = os.path.splitext(i)
            identity = fname.split("_")[1]
            try:
                sid = Student.query.filter_by(identity=identity).first().id
            except AttributeError:
                print(i)
                continue
            if "fmat" != "jpg":
                image = Image.open(i)
                image = image.convert('RGB')
                image.save(sid + "." + "jpg")
                os.remove(i)
            else:
                os.rename(i, sid + "." + fmat)