# coding=utf-8

from flask import Blueprint
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from jinja2 import TemplateNotFound

from koromon.account.models import User, Role
from koromon.exts.rbac import rbac
from koromon.pages.models import Pages, Config
from koromon.utils.resp import is_setup

views = Blueprint('pages', __name__)


@views.route('/setup', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], methods=['GET'])
def setup():
    if not is_setup():
        if request.method == 'POST':
            # Admin user
            login_name = request.form['login_name']
            print login_name
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
        page = Pages.query.filter_by(route=template).first()
        if page:
            return render_template('page.html', content=page.html)
        else:
            abort(404)
