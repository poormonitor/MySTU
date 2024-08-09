from . import db


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(8))
    cls = db.Column(db.String(16), index=True)
    sex = db.Column(db.Integer)
    phone = db.Column(db.String(16))
    people = db.Column(db.String(8))
    domicile = db.Column(db.String(8))
    party = db.Column(db.String(8))
    religion = db.Column(db.String(8))
    identity = db.Column(db.String(24))
    bank = db.Column(db.String(16))
    domitory = db.Column(db.String(32), index=True)
    bed = db.Column(db.String(8))
    qq = db.Column(db.String(16))
    email = db.Column(db.String(64))
    residence = db.Column(db.String(64))
    contact = db.Column(db.String(32))
    fcontact1 = db.Column(db.String(8))
    fcontact1phone = db.Column(db.String(16))
    fcontact2 = db.Column(db.String(8))
    fcontact2phone = db.Column(db.String(16))
    memo = db.Column(db.Text)
    memoupdate = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return "<Student %r>" % self.name

    def __init__(self, *args):
        (
            self.id,
            self.name,
            self.sex,
            self.cls,
            self.party,
            self.people,
            self.religion,
            self.identity,
            self.bank,
            self.phone,
            self.email,
            self.qq,
            self.domitory,
            self.bed,
            self.contact,
            self.domicile,
            self.fcontact1,
            self.fcontact1phone,
            self.fcontact2,
            self.fcontact2phone,
            self.residence,
            self.memo,
        ) = args

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
