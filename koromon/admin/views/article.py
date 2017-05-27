from flask_login import login_required

from koromon.admin.views.main import bp as admin_bp
from koromon.exts.rbac import rbac


@admin_bp.route("/article/add/", methods=['POST'])
@rbac.allow(['superuser'], methods=['GET'])
@login_required
def add(id):
    pass


@admin_bp.route("/article/delete/<int:id>", methods=['GET'])
@rbac.allow(['superuser'], methods=['GET'])
@login_required
def delete(id):
    pass
