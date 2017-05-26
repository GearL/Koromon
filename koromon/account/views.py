from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user

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


@bp.route("/logout", methods=['POST'])
@rbac.allow(['anonymous'], ['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('account.sign_in'))


@bp.route("/detail", methods=['GET', 'POST'])
@rbac.allow(['superuser', 'manager'], methods=['GET', 'POST'])
@login_required
def profile():
    pass
