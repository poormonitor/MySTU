from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    passwd = db.Column(db.String(64), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<User %r>" % self.id

    def __init__(self, id, name, password, admin=False):
        self.id = id
        self.name = name
        self.passwd = password
        self.admin = admin

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}