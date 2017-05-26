from flask import Blueprint

from koromon.exts.rbac import rbac

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/signin', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def sign_in():
    pass


@bp.route('/signup', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def sign_up():
    pass
