# coding=utf-8
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from koromon.admin.models import Config
from koromon.admin.views.main import bp as admin
from koromon.exts.rbac import rbac
from koromon.pages.models import Pages
from koromon.utils.resp import success


@admin.route('/admin/pages', defaults={'route': None}, methods=['GET', 'POST'])
@admin.route('/admin/pages/<route>', methods=['GET', 'POST'])
@rbac.allow(['superuser'], methods=['GET', 'POST'])
def admin_pages(route):
    if request.method == 'GET' and request.args.get('mode') == 'create':
        return render_template('admin/editor.html')
    if route and request.method == 'GET':
        page = Pages.get_by_route(route)
        return render_template('admin/editor.html', page=page)
    if route and request.method == 'POST':
        page = Pages.get_by_route(route)
        errors = []
        html = request.form['html']
        route = request.form['route']
        if not route:
            errors.append({'route': 'Missing URL route'})
        if errors:
            page = Pages(html, '')
            return render_template('/admin/editor.html', page=page)
        if page:
            page.route = route
            page.html = html
            page.save()
            return redirect(url_for('admin.admin_pages'))
        page = Pages(route, html)
        page.save()
        return redirect(url_for('admin.admin_pages'))
    pages = Pages.query.all()
    return render_template(
        'admin/pages.html',
        routes=pages,
        css=Config.get_config('css')
    )


@admin.route('/admin/page/<page_route>/delete', methods=['POST'])
@rbac.allow(['superuser'], methods=['GET', 'POST'])
def delete_page(page_route):
    page = Pages.get_by_route(page_route)
    page.delete()
    return success(message=u'删除成功')
