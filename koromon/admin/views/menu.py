# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required

from koromon.exts.rbac import rbac
from koromon.menu.models import Menu
from koromon.utils.resp import success, fail

bp = Blueprint('admin_menu', __name__, url_prefix='/admin/menu')


@bp.route('', methods=['GET'])
@login_required
@rbac.allow(['superuser', 'manager'], methods=['GET'])
def menu_list():
    first_level_menus = Menu.get_by_type(menu_type=1)
    menus = []
    for first_menu in first_level_menus:
        first_menu_json = first_menu.jsonify()
        menu_id = first_menu.id
        second_level_menus = Menu.get_by_parent_id(parent_id=menu_id)
        first_menu_json['second_menu'] = []
        for second_menu in second_level_menus:
            first_menu_json['second_menu'].append(second_menu.jsonify())
        menus.append(first_menu_json)
    return render_template('admin/menu/list.html', menus=menus)


@bp.route('', methods=['POST'])
@login_required
@rbac.allow(['superuser', 'manager'], methods=['POST'])
def add():
    menu_name = request.form.get('name')
    menu_url = request.form.get('url')
    menu_type = request.form.get('type', default=1, type=int)
    menu_sort = request.form.get('sort', default=0, type=int)
    menu_parent_id = request.form.get('parent_id', default=0, type=int)
    flag = False
    errors = {}
    if (menu_type == 2 and menu_parent_id == 0) \
            or (menu_type not in range(1, 3)) \
            or (menu_type == 1 and menu_parent_id != 0):
        flag = True
        errors['type_error'] = u'目录类型有误'
    menu = Menu.get_by_id(menu_parent_id)
    if menu is None:
        flag = True
        errors['parent_id_error'] = u'一级目录有误'
    if len(menu_url) > 512:
        flag = True
        errors['menu_url_error'] = u'url长度有误,长度应小于512字符'
    if flag is True:
        return fail(result=errors)
    menu = Menu(
        name=menu_name,
        url=menu_url,
        type=menu_type,
        sort=menu_sort,
        parent_id=menu_parent_id
    )
    menu.save()
    return success(message=u'添加成功')


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
@rbac.allow(['superuser', 'manager'], methods=['DELETE'])
def delete(id):
    menu = Menu.get_by_id(id)
    if menu is None:
        return fail(message=u'目录不存在')
    menu.delete()
    return success(message=u'删除成功')


@bp.route('/<int:id>', methods=['PATCH'])
@login_required
@rbac.allow(['superuser', 'manager'], methods=['PATCH'])
def update(id):
    menu = Menu.get_by_id(id)
    if menu is None:
        return fail(message=u'目录不存在')
    menu.update(request.form)
    return success(message=u'更新成功')
