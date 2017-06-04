# coding=utf-8
from flask import Blueprint
from flask import render_template
from flask import request
from flask.ext.login import login_required

from koromon.article.models import Category
from koromon.exts.rbac import rbac
from koromon.utils.resp import success, fail

bp = Blueprint('admin_category', __name__, url_prefix='/admin/category')


@bp.route('', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def category_list():
    page = request.args.get('page', default=1, type=int)
    limit = 10
    categories = Category.paginate(page=page, per_page=limit)

    if page != 1:
        lists = []
        for category in categories.items:
            lists.append(category.jsonify())
        return success(result=lists)

    return render_template(
        'admin/article/category_list.html',
        categories=categories.items
    )


@bp.route('', methods=['POST'])
@rbac.allow(['superuser', 'manager'], methods=['POST'])
@login_required
def add():
    category_name = request.form.get('category_name')
    category_url = request.form.get('category_url')
    if category_name is None or category_url is None:
        return fail(message=u'请求参数不完整')
    category_by_name = Category.get_by_name(category_name)
    category_by_url = Category.get_by_url(category_url)
    if category_by_name is not None:
        return fail(message=u'分类名已存在')
    if category_by_url is not None:
        return fail(message=u'url已存在')
    category = Category(
        name=category_name,
        url=category_url
    )
    category.save()
    return success(message=u'添加成功')


@bp.route('/<int:id>', methods=['DELETE'])
@rbac.allow(['superuser', 'manager'], methods=['DELETE'])
@login_required
def delete(id):
    category = Category.get_by_id(id)
    if category is not None:
        category.delete()
        return success(message=u'删除成功')
    return fail(message=u'分类不存在')


@bp.route('/<int:id>', methods=['PATCH'])
@rbac.allow(['superuser', 'manager'], methods=['PATCH'])
@login_required
def update(id):
    category = Category.get_by_id(id)
    if category is not None:
        category.update(request.form)
        return success(message=u'修改成功')
    return fail(message=u'分类不存在')
