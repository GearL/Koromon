# coding=utf-8
from flask import render_template
from flask import request
from flask import url_for

from koromon.admin.models import Config
from koromon.admin.views.main import bp as admin
from koromon.exts.rbac import rbac
from koromon.page.models import Pages
from koromon.utils.resp import success, fail


@admin.route('/pages', defaults={'route': None}, methods=['GET'])
@admin.route('/pages/<route>', methods=['GET'])
@rbac.allow(['superuser'], methods=['GET'])
def get_pages(route):
    if request.args.get('mode') == 'create':
        return render_template('admin/editor.html')
    if route:
        page = Pages.get_by_route(route)
        return render_template('admin/editor.html', page=page)
    pages = Pages.query.all()
    return render_template(
        'admin/pages.html',
        routes=pages,
        css=Config.get_config('css')
    )


@admin.route('/pages/<route>', methods=['POST'])
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
                    'redirect_url': url_for('admin.get_pages')
                }
            )
        page = Pages(route, html)
        page.save()
        return success(
            result={
                'redirect_url': url_for('admin.get_pages')
            }
        )


@admin.route('/page/<page_route>/delete', methods=['POST'])
@rbac.allow(['superuser'], methods=['GET', 'POST'])
def delete_page(page_route):
    page = Pages.get_by_route(page_route)
    page.delete()
    return success(message=u'删除成功')
