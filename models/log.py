from datetime import datetime, timezone

from . import db


class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(32), index=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    indate = db.Column(db.DateTime)
    user = db.Column(db.String(32))

    def __repr__(self):
        return "<Log %r>" % self.id

    def __init__(self, title, content, user, student):
        self.title = title
        self.content = content
        self.user = user
        self.student = student
        self.indate = datetime.now(timezone.utc)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
