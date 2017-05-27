from koromon.exts.database import db
from koromon.common.models import Base


class Pages(Base):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(80), unique=True)
    html = db.Column(db.Text)

    def __init__(self, route, html):
        self.route = route
        self.html = html

    @classmethod
    def get_by_route(cls, route):
        return cls.query.filter_by(route=route).first()
