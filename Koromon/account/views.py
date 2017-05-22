from flask import Blueprint

from Koromon.exts import rbac

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route("/signin", methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def SignIn():
    pass


@bp.route("/signup", methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def SignUp():
    pass
