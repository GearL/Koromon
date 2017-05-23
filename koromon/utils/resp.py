import hashlib

from flask import jsonify

from koromon.pages.models import Config


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


def sha512(string):
    return hashlib.sha512(string).hexdigest()


def is_setup():
    setup = Config.query.filter_by(key='setup').first()
    if setup:
        return setup.value
    else:
        return False
