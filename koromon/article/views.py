# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, abort
from flask import render_template
from flask import request

from koromon.article.models import Article, Category
from koromon.exts.rbac import rbac
from koromon.utils.resp import success, fail

bp = Blueprint('article', __name__, url_prefix='/categories')


@bp.route('/<string:category>/articles/', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def article_list(category):
    page = request.args.get('page', default=1, type=int)
    limit = 10
    category = Category.get_by_url(category)
    if category is not None:
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
    abort(404)


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
    if category is not None:
        category_id = category.id
        art = Article.get_by_two_id(article_id=article_id, category_id=category_id)
        if art is not None:
            return render_template('article/detail.html', article=art)
    abort(404)

