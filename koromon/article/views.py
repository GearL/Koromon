# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from koromon.article.models import Article, Category
from koromon.exts.rbac import rbac
from koromon.utils.resp import success

bp = Blueprint('article', __name__, url_prefix='/categories')


@bp.route('/<string:category>/articles/', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def article_list_for_category(category):
    page = request.args.get('page', default=1, type=int)
    limit = 10
    category = Category.get_by_url(category)
    category_id = category.id
    filte = 'category_id=%d' % category_id
    articles = Article.paginate(
        page=page,
        per_page=limit,
        filters=[filte],
        order_by='-top, -modified'
    )
    if page != 1:
        article_json = []
        for art in articles.items:
            article_json.append(art.jsonify())
        return success(result=article_json)
    return render_template(
        'artcile/list_by_category.html',
        articles=articles.items,
        total=articles.total
    )


@bp.route('/articles', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def article_list():
    page = request.args.get('page', default=1, type=int)
    limit = 10
    articles = Article.paginate(
        page=page,
        per_page=limit,
        order_by='-top, -modified'
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


@bp.route('/<string:category>/<int:article_id>/', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def detail(category, article_id):
    category = Category.get_by_url(category)
    category_id = category.id
    art = Article.get_by_two_id(
        article_id=article_id,
        category_id=category_id
    )
    return render_template('article/detail.html', article=art)
