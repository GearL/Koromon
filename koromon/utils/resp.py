from flask import jsonify

from koromon.admin.models import Config
from koromon.article.models import Category


def success(message='', result={}):
    return jsonify(
        success=True,
        message=message,
        result=result
    )


def fail(message='', result={}):
    return jsonify(
        success=False,
        message=message,
        result=result
    )


def is_ajax(req):
    return req.headers.get('X-Requested-With') is not None


def is_setup():
    setup = Config.get_by_key('setup')
    if setup:
        return setup.value
    else:
        return False


def get_choice():
    choices = {}
    categories = Category.get_all()
    for category in categories:
        choices[category.id] = category.name
    return choices
