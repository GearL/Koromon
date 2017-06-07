# -*- coding: utf-8 -*-
"""
    错误返回信息可以自己定制
    validators.xx(xx, message='something')
    这样如果不符合要求的话就会返回message的内容
    eg:
    password = PasswordField(
        label=u'密码',
        validators=[
            validators.length(min=6, max=16, message=u'长度要求在6～16个字符'）
        ]
    )
    如果我们输入字符长度不在6～16区间内的，就会返回 长度要求在6～16个字
    返回内容会在 form.errors.password
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators


class SignInForm(FlaskForm):
    login_name = StringField(
        label=u'登录名',
        description=u'4～16个字符',
        validators=[
            validators.InputRequired(),
            validators.length(min=4, max=16),
        ]
    )
    password = PasswordField(
        label=u'密码',
        description=u'6~16个字符',
        validators=[
            validators.InputRequired(),
            validators.length(min=6, max=16)
        ]
    )
    remember = BooleanField(u'记住我')


class SignUpForm(FlaskForm):
    login_name = StringField(
        label=u'登录名',
        validators=[
            validators.length(min=4, max=16)
        ]
    )
    nickname = StringField(
        label=u'显示名',
        validators=[
            validators.length(min=4, max=24)
        ]
    )
    password = PasswordField(
        label=u'密码',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16)
        ]
    )
    confirm_password = PasswordField(
        label=u'确认密码',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16)
        ]
    )


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        label=u'旧密码',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16)
        ]
    )
    new_password = PasswordField(
        label=u'新密码',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16)
        ]
    )
    confirm_password = PasswordField(
        label=u'确认密码',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16),
            validators.equal_to('newpassword', message=u'新密码与确认密码不匹配')
        ]
    )


class ReSetPasswordForm(FlaskForm):
    email = StringField(
        label=u'邮箱',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16)
        ]
    )
    newpassword = PasswordField(
        label=u'新密码',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16)
        ]
    )
    confirm_password = PasswordField(
        label=u'确认密码',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16),
            validators.equal_to('newpassword', message=u'新密码与确认密码不匹配')
        ]
    )


class DetailForm(FlaskForm):
    nickname = StringField(
        label=u'显示名',
        validators=[
            validators.length(min=4, max=24)
        ]
    )
    email = StringField(
        label=u'邮箱',
        validators=[
            validators.DataRequired(),
            validators.length(min=6, max=16)
        ]
    )
    qq = StringField(
        label=u'qq',
        validators=[
            validators.DataRequired(),
            validators.length(min=7, max=11)
        ]
    )
    phone = StringField(
        label=u'手机',
        validators=[
            validators.DataRequired(),
            validators.length(min=11, max=11)
        ]
    )
