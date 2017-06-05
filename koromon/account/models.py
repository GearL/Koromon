# -*- coding: utf-8 -*-
import urllib
from datetime import datetime
from hashlib import md5, sha256
from uuid import uuid4

from flask_rbac import RoleMixin, UserMixin
from flask_sqlalchemy import BaseQuery

from koromon.exts.database import db
from koromon.utils.resp import fail, success
from koromon.common.models import Base


class UserQuery(BaseQuery):
    def authenticate(self, login_name, raw_password):
        user = self.filter(User.login_name == login_name).first()
        if user and user.check_password(raw_password):
            return user
        return None


roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('role.id'))
)

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(RoleMixin, Base):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    parents = db.relationship(
        'Role',
        secondary=roles_parents,
        primaryjoin=(id == roles_parents.c.role_id),
        secondaryjoin=(id == roles_parents.c.parent_id),
        backref=db.backref('children', lazy='dynamic')
    )
    users = db.relationship('User', secondary=users_roles,
                            backref=db.backref('roles', lazy='dynamic'))

    def __init__(self, name):
        RoleMixin.__init__(self)
        self.name = name

    def add_parent(self, parent):
        # You don't need to add this role to parent's children set,
        # relationship between roles would do this work automatically
        self.parents.append(parent)

    def add_parents(self, *parents):
        for parent in parents:
            self.add_parent(parent)

    def get_users(self):
        users = []
        for user in self.users:
            users.append(user.jsonify())
        return users

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class User(UserMixin, Base):
    """Model of user."""

    __tablename__ = 'user'
    query_class = UserQuery
    USER_STATE_VALUES = ('normal', 'frozen', 'deleted', 'unactivated')
    USER_STATE_TEXTS = ('Normal', 'Frozen',
                        'Deleted', 'Unactivated')

    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(30), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64))
    nickname = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    qq = db.Column(db.String(15), nullable=True)
    avatar = db.Column(db.String(250))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    salt = db.Column(db.String(32), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    state = db.Column(db.Enum(*USER_STATE_VALUES), default='unactivated')

    def __init__(self, **kwargs):
        self.salt = uuid4().hex

        if 'login_name' in kwargs:
            login_name = kwargs.pop('login_name')
            self.login_name = login_name.lower()

        if 'password' in kwargs:
            raw_password = kwargs.pop('password')
            self.change_password(raw_password)

        if 'nickname' in kwargs:
            nickname = kwargs.pop('nickname')
            self.nickname = nickname.lower()

        db.Model.__init__(self, **kwargs)

    def __unicode__(self):
        return self.login_name

    def __repr__(self):
        return '<User: %s>' % self.login_name

    def change_password(self, raw_password):
        self.salt = uuid4().hex
        self.hashed_password = self._hash_password(self.salt, raw_password)

    def check_password(self, raw_password):
        _hashed_password = self._hash_password(self.salt, raw_password)
        return self.hashed_password == _hashed_password

    def has_email(self):
        return self.email is not None

    def check_email(self, email):
        return self.email == email

    def check_state(self):
        return self.state

    def is_active(self):
        return self.state == 'normal'

    def is_anonymous(self):
        return self.nickname is None

    def get_id(self):
        return self.id

    def get_role(self):
        if self.role.name == u'superuser':
            return u'超级管理员'
        elif self.role.name == u'manager':
            return u'管理员'

    def jsonify(self):
        return {
            'id': self.id,
            'login_name': self.login_name,
            'nickname': self.nickname,
            'email': self.email,
            'qq': self.qq,
            'phone': self.phone,
            'create_date': self.created,
            'state': self.state,
            'avatar': self.get_avatar(),
            'role': self.role.name
        }

    def is_authenticated(self):
        return self.state in ('normal', 'unactivated')

    def active(self):
        self.state = 'normal'

    def set_state(self, state):
        if state in self.USER_STATE_VALUES:
            self.state = state

    def get_avatar(self, size=70):
        if self.avatar:
            return self.avatar

        if not self.email:
            self.email = 'None'
        url_pattern = 'http://www.gravatar.com/avatar/%s?%s'
        gravatar_url = url_pattern % (md5(self.email.lower()).hexdigest(),
                                      urllib.urlencode({'s': str(size)}))
        return gravatar_url

    def set_avatar(self, avatar_url):
        self.avatar = avatar_url

    @property
    def role(self):
        return Role.get_by_id(self.role_id)

    @classmethod
    def check_login_name(cls, login_name):
        if cls.get_by_login_name(login_name):
            return fail(message=u'用户已存在')
        return success(message=u'用户名可用')

    @classmethod
    def get_by_login_name(cls, login_name):
        return cls.query.filter_by(login_name=login_name).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @staticmethod
    def _hash_password(salt, password):
        hashed = sha256()
        hashed.update('<%s|%s>' % (salt, password))
        return hashed.hexdigest()
