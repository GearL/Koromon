# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask import abort

from koromon.article.models import Article, Category
from koromon.exts.rbac import rbac
from koromon.utils.resp import success, fail

bp = Blueprint('article', __name__, url_prefix='/categories')


@bp.route('/<string:category>/articles/', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def article_list(category):
    category = Category.get_category_by_url_string(category)
    if category is not None:
        category_id = category.id
        article_json = Article.get_article_json_by_category_id(category_id)
        return jsonify(article_json)
    abort(404)


@bp.route('/<string:category>/<int:article_id>/', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def article(category, article_id):
    category = Category.get_category_by_url_string(category)
    if category is not None:
        category_id = category.id
        art = Article.query.filter_by(
            category_id=category_id,
            id=article_id
        ).first()
        return jsonify(art.jsonify())
    abort(404)


@bp.route('/<string:category>/delete/', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def delete(category):
    category = Category.get_category_by_url_string(category)
    flag = category.delete(commit=True)
    if flag:
        return success(message=u'删除成功')
    else:
        return fail(message=u'删除失败')
