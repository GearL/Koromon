from flask import Blueprint

from koromon.exts.rbac import rbac
from koromon.menu.models import Menu
from koromon.utils.resp import success

bp = Blueprint('menu', __name__, url_prefix='/menu')


@bp.route('', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
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
    return success(result=menus)
