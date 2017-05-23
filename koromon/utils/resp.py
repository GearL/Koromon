from flask import jsonify


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
