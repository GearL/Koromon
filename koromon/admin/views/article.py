# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required

from koromon.article.forms import ArticleForm
from koromon.article.models import Article
from koromon.exts.rbac import rbac
from koromon.utils.resp import success, fail, get_choice

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
    form = ArticleForm()
    category_choice = get_choice()  # 选择文章分类
    return render_template(
        'admin/article/editor.html',
        form=form,
        choice=category_choice
    )


@bp.route('/', methods=['POST'])
@rbac.allow(['superuser', 'manager'], methods=['POST'])
@login_required
def add():
    form = ArticleForm(request.form)
    if form.validate():
        article = Article(
            name=form.name,
            description=form.description,
            content=form.content
        )
        article.save()
        return success(message=u'添加成功')
    if form.errors:
        return fail(result=form.errors)


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
    form = ArticleForm(request.form)
    if 'category' in request.form:
        category_id = request.form.get(
            'category',
            default=article.category_id,
            type=int
        )
        article.update({'category_id': category_id})
    if form.validate():
        article.update(form.data)
    return success(message=u'修改成功')


@bp.route('/<int:id>', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def detail(id):
    article = Article.get_by_id(id)
    form = ArticleForm()
    category_choice = get_choice()
    return render_template(
        'admin/article/editor.html',
        article=article,
        form=form,
        choice=category_choice
    )


@bp.route('/<int:id>', methods=['POST'])
@rbac.allow(['superuser', 'manager'], methods=['POST'])
@login_required
def set_top(id):
    article = Article.get_by_id(id)
    article.set_top()
    return success(message=u'置顶成功')
