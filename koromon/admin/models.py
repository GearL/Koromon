from koromon.common.models import Base
from koromon.exts.database import db


class Config(Base):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @classmethod
    def get_by_key(cls, key):
        return cls.query.filter_by(key=key).first()
