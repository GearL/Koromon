from koromon.utils.json import success, fail


def is_ajax(req):
    return req.headers.get('X-Requested-With') is not None
