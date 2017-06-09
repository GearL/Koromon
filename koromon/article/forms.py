# coding=utf-8
"""
    那个错误返回信息可以自己定制
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
from wtforms import StringField, validators


class ArticleForm(FlaskForm):
    name = StringField(
        label=u'文章标题',
        description=u'1～32个字符',
        validators=[
            validators.InputRequired(),
            validators.length(min=1, max=32, message=u'标题长度要求在1~32个字符'),
        ]
    )
    description = StringField(
        label=u'文章简介',
        description=u'0~144个字符',
        validators=[
            validators.InputRequired(),
            validators.length(max=144, message=u'简介长度不得超过144个字符')
        ]
    )
    content = StringField(
        label=u'文章内容',
        validators=[
            validators.InputRequired()
        ]
    )
