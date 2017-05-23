from sqlalchemy.exc import IntegrityError

from koromon.exts.database import db


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Pages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(80), unique=True)
    html = db.Column(db.Text)

    def __init__(self, route, html):
        self.route = route
        self.html = html

