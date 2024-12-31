from datetime import datetime, timezone

from . import db


class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.String(32), primary_key=True)
    score = db.Column(db.Text, default="[]")
    unqualified = db.Column(db.Text, default="[]")
    attendance = db.Column(db.Text, default="[]")
    award = db.Column(db.Text, default="[]")
    warning = db.Column(db.Text, default="[]")
    last_update = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return "<Record %r>" % self.id

    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
