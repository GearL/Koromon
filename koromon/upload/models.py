from datetime import datetime

from koromon.common.models import Base
from koromon.exts.database import db


class UploadFile(Base):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64), unique=True)
    file_path = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return '%s' % self.file_name

    def __repr__(self):
        return '<Category %s>' % self.file_name

    @classmethod
    def check_file_name(cls, file_name):
        uploaded_file = cls.query.filter_by(file_name=file_name).first()
        if uploaded_file is None:
            return True
        return False
