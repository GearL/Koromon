# coding=utf-8

from flask import Blueprint, abort, redirect
from flask import url_for, render_template, request
from jinja2 import TemplateNotFound

from koromon.account.models import User, Role
from koromon.exts.rbac import rbac
from koromon.page.models import Pages
from koromon.admin.models import Config
from koromon.utils.resp import is_setup

views = Blueprint('pages', __name__)


@views.route('/setup', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], methods=['GET', 'POST'])
def setup():
    if not is_setup():
        if request.method == 'POST':
            # Admin user
            login_name = request.form['login_name']
            nickname = request.form['nickname']
            password = request.form['password']
            admin = User(
                login_name=login_name,
                nickname=nickname,
                passwd=password
            )
            super_user = Role.get_by_name('superuser')
            admin.roles.append(super_user)
            admin.save()
            Config('setup', True).save()
            return redirect(url_for('pages.static_html'))
        return render_template('setup.html')
    return redirect(url_for('pages.static_html'))


@views.route("/", defaults={'template': 'index'})
@views.route("/<template>")
@rbac.allow(['anonymous'], methods=['GET'])
def static_html(template):
    try:
        return render_template('%s.html' % template)
    except TemplateNotFound:
        page = Pages.get_by_route(template)
        if page:
            return render_template('page.html', content=page.html)
        else:
            abort(404)
