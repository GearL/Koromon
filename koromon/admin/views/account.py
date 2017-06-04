# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required

from koromon.account.models import Role, User
from koromon.exts.rbac import rbac
from koromon.utils.resp import success, fail

bp = Blueprint('admin_account', __name__, url_prefix='/admin/account')


@bp.route('', methods=['GET'])
@rbac.allow(['superuser'], methods=['GET'])
@login_required
def account_list():
    page = request.args.get('page', default=1, type=int)
    limit = 10
    user_list = User.paginate(page=page, per_page=limit)

    if page != 1:
        users = []
        for user in user_list.items:
            users.append(user.jsonify())
        return success(
            result=users
        )
    return render_template(
        'admin/account/list.html',
        users=user_list.items,
        total=user_list.total
    )


@bp.route('/manager/<int:id>', methods=['POST'])
@rbac.allow(['superuser'], methods=['POST'])
@login_required
def add_manager(id):
    user = User.get_by_id(id)

    if user is not None:
        manager = Role.get_by_name('manager')
        user.roles.remove(Role.get_by_id(user.role_id))
        user.roles.append(manager)
        user.role_id = manager.id
        user.save()
        return success(message=u'设置管理员成功')

    return fail(message=u'用户不存在')


@bp.route('/manager/<int:id>', methods=['DELETE'])
@rbac.allow(['superuser'], methods=['DELETE'])
@login_required
def delete_manager(id):
    user = User.get_by_id(id)
    if user is not None:
        normal = Role.get_by_name('normal')
        user.roles.remove(Role.get_by_id(user.role_id))
        user.role_id = normal.id
        user.roles.append(normal)
        user.save()
        return success(message=u'取消管理员成功')
    return fail(message=u'用户不存在')


@bp.route('/<int:id>', methods=['POST'])
@rbac.allow(['superuser', 'manager'], methods=['POST'])
@login_required
def account(id):
    user = User.get_by_id(id)
    if user is None:
        return fail(message=u'用户不存在')
    state = request.form.get('state', 'None')
    if state is not 'None':
        if state in User.USER_STATE_VALUES:
            user.state = state
            user.save()
            return success(message=u'操作成功')
    return fail(message=u'请求参数有误')
