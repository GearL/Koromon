from flask_login import login_required

from koromon.admin.views.main import bp as admin_bp
from koromon.exts.rbac import rbac


@admin_bp.route("/manager/<int:id>", methods=['POST'])
@rbac.allow(['superuser'], methods=['POST'])
@login_required
def add_manager(id):
    pass


@admin_bp.route("/manager/<int:id>", methods=['GET'])
@rbac.allow(['superuser'], methods=['GET'])
@login_required
def manager_list(id):
    pass


@admin_bp.route("/manager/<int:id>", methods=['DELETE'])
@rbac.allow(['superuser'], methods=['DELETE'])
@login_required
def delete_manager(id):
    pass
