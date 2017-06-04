from datetime import datetime

from sqlalchemy.exc import IntegrityError

from koromon.common.models import Base
from koromon.exts.database import db


class Category(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    url_string = db.Column(db.String(16), unique=True)
    articles = db.relationship('Article', backref='category')
    deleted = db.Column(db.BOOLEAN, default=False)

    def __str__(self):
        return '%s' % self.name

    def __repr__(self):
        return '<Category %s>' % self.name

    def jsonify(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url_string
        }

    def delete(self, commit=True):
        for article in self.articles:
            article.delete(False)
        self.deleted = True
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
                return True
            except IntegrityError:
                db.session.rollback()
                return False

    @classmethod
    def get_by_id(cls, id):
        category = cls.query.filter_by(
            id=id,
            deleted=False
        ).first()
        return category

    @classmethod
    def get_by_url(cls, url_string):
        category = cls.query.filter_by(
            url_string=url_string,
            deleted=False
        ).first()
        return category

    @classmethod
    def get_by_name(cls, name):
        category = cls.query.filter_by(
            url_string=name,
            deleted=False
        ).first()
        return category


class Article(Base):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(144))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    deleted = db.Column(db.BOOLEAN, default=False)

    def __str__(self):
        return '%s' % self.name

    def __repr__(self):
        return '<Article %s>' % self.name

    def jsonify(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'content': self.content,
            'created': self.created,
            'modified': self.modified,
            'category_id': self.category_id,
        }

    @classmethod
    def get_article_json_by_category_id(cls, category_id):
        articles = cls.query.filter_by(category_id=category_id, deleted=False)
        article_json = {}
        for art in articles:
            article_json[art.name] = art.jsonify()
        return article_json
