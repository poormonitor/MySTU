from . import db


class Weixin(db.Model):
    __tablename__ = "weixin"
    openid = db.Column(db.String(128), primary_key=True)
    role = db.Column(db.Integer, nullable=False)
    attach = db.Column(db.String(32), nullable=False)
    nick = db.Column(db.String(32), nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)


    def __repr__(self):
        return "<Weixin %r>" % self.openid

    def __init__(self, openid, role, attach, nick):
        self.openid = openid
        self.role = role
        self.attach = attach
        self.nick = nick

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}