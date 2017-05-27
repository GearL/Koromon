from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required, current_user

from koromon.exts.rbac import rbac

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/index', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def index():
    if current_user.is_anonymous():
        return redirect(url_for('account.sign_in'))
    return render_template('admin/index.html')
