# coding=utf-8
from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import login_required

from koromon.article.models import Article
from koromon.exts.rbac import rbac
from koromon.utils.resp import success, fail

bp = Blueprint('admin_article', __name__, url_prefix='/admin/article')


@bp.route('', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def article_list():
    page = request.args.get('page', default=1, type=int)
    limit = 10
    articles = Article.paginate(
        page=page,
        per_page=limit,
        order_by='-id'
    )
    if page != 1:
        article_json = []
        for art in articles.items:
            article_json.append(art.jsonify())
        return success(result=article_json)
    return render_template(
        'artcile/list_all.html',
        articles=articles.items,
        total=articles.total
    )


@bp.route('/', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def editor():
    return render_template('admin/article/editor.html')


@bp.route('/', methods=['POST'])
@rbac.allow(['superuser', 'manager'], methods=['POST'])
@login_required
def add():
    name = request.form.get('name')
    description = request.form.get('description')
    content = request.form.get('content')
    errors = {}
    error = False
    if name is None:
        error = True
        error['name_error'] = u'缺少文章名'
    if description is None:
        error = True
        error['description_error'] = u'缺少文章简介'
    if content is None:
        error = True
        error['content_error'] = u'缺少文章内容'
    if error is True:
        return fail(result=errors)
    article = Article(name=name, description=description, content=content)
    article.save()
    return success(message=u'添加成功')


@bp.route('/<int:id>', methods=['DELETE'])
@rbac.allow(['superuser', 'manager'], methods=['DELETE'])
@login_required
def delete(id):
    article = Article.get_by_id(id)
    article.delete()
    return success(message=u'删除成功')


@bp.route('/<int:id>', methods=['PATCH'])
@rbac.allow(['superuser', 'manager'], methods=['PATCH'])
@login_required
def update(id):
    article = Article.get_by_id(id)
    article.update(request.form)
    return success(message=u'修改成功')


@bp.route('/<int:id>', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def detail(id):
    article = Article.get_by_id(id)
    return render_template('admin/article/editor.html', article=article)


@bp.route('/<int:id>', methods=['POST'])
@rbac.allow(['superuser', 'manager'], methods=['POST'])
@login_required
def set_top(id):
    article = Article.get_by_id(id)
    article.set_top()
    return success(message=u'置顶成功')
