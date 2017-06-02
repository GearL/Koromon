from flask import Blueprint
from flask_login import login_required

from koromon.exts.rbac import rbac

bp = Blueprint('admin_article', __name__, url_prefix='/admin/article')


@bp.route('/article/add/', methods=['POST'])
@rbac.allow(['superuser'], methods=['GET'])
@login_required
def add(id):
    pass


@bp.route('/article/delete/<int:id>', methods=['GET'])
@rbac.allow(['superuser'], methods=['GET'])
@login_required
def delete(id):
    pass
