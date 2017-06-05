# coding=utf-8
from flask import Blueprint, render_template, request
from flask import url_for

from koromon.admin.models import Config
from koromon.exts.rbac import rbac
from koromon.page.models import Pages
from koromon.utils.resp import success, fail

bp = Blueprint('admin_page', __name__, url_prefix='/admin/page')


@bp.route('/', defaults={'route': None}, methods=['GET'])
@bp.route('/<route>', methods=['GET'])
@rbac.allow(['superuser'], methods=['GET'])
def get_pages(route):
    if request.args.get('mode') == 'create':
        return render_template('bp/editor.html')
    if route:
        page = Pages.get_by_route(route)
        return render_template('bp/editor.html', page=page)
    pages = Pages.query.all()
    return render_template(
        'bp/pages.html',
        routes=pages,
        css=Config.get_config('css')
    )


@bp.route('/<route>', methods=['POST'])
@rbac.allow(['superuser'], methods=['POST'])
def update_pages(route):
    if route:
        page = Pages.get_by_route(route)
        errors = []
        html = request.form['html']
        route = request.form['route']
        if not route:
            errors.append({'route': 'Missing URL route'})
        if errors:
            return fail(
                result={
                    'errors': errors
                }
            )
        if page:
            page.route = route
            page.html = html
            page.save()
            return success(
                result={
                    'redirect_url': url_for('bp.get_pages')
                }
            )
        page = Pages(route, html)
        page.save()
        return success(
            result={
                'redirect_url': url_for('bp.get_pages')
            }
        )


@bp.route('/<route>', methods=['DELETE'])
@rbac.allow(['superuser'], methods=['DELETE'])
def delete_page(route):
    page = Pages.get_by_route(route)
    page.delete()
    return success(message=u'删除成功')
