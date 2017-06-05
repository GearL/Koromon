# coding=utf-8
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from koromon.common.models import Base
from koromon.exts.database import db


class Menu(Base):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    type = db.Column(db.Integer, default=1)  # 默认为1，1为一级目录，2为二级目录，不支持更高级目录
    sort = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, default=0)  # 区分二级目录归在哪个一级目录下
    url = db.Column(db.String(512))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.BOOLEAN, default=False)

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return "<Menu %s>" % self.name

    def delete(self, commit=True):
        menus = Menu.query.filter_by(parent_id=self.id)
        for menu in menus:
            menu.delete(commit=False)
        self.deleted = True
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
                return True
            except IntegrityError:
                db.session.rollback()
                return False

    def jsonify(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'sort': self.sort,
            'parent_id': self.parent_id,
            'url': self.url
        }

    @classmethod
    def get_by_type(cls, menu_type):
        return Menu.query.filter_by(
            type=menu_type,
            deleted=False
        ).order_by('sort')

    @classmethod
    def get_by_id(cls, menu_id):
        return Menu.query.filter_by(
            id=menu_id,
            deleted=False
        ).first()

    @classmethod
    def get_by_parent_id(cls, parent_id):
        return Menu.query.filter_by(
            parent_id=parent_id,
            deleted=False
        ).order_by('sort')
