# coding=utf-8
from flask import Blueprint, redirect, url_for
from flask import render_template
from flask import request
from flask_login import current_user, login_user
from flask_login import login_required, logout_user

from koromon.account.forms import SignInForm
from koromon.account.models import User
from koromon.exts.rbac import rbac
from koromon.utils.resp import fail, success

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/signin', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def sign_in():
    if not current_user.is_anonymous():
        return redirect(url_for('admin.index'))

    form = SignInForm()

    if form.validate_on_submit():
        login_name = request.form['loginname'].strip()
        password = request.form['passwd'].strip()
        is_remember = False
        if 'remember' in request.form:
            is_remember = request.form['remember']
        user = User.query.authenticate(login_name, password)
        if user:
            if not user.is_active():
                return fail(
                    message=u'用户已被暂停使用,请联系管理员'
                )
            login_user(user, remember=is_remember, force=True)
            return success(
                message=u'登录成功',
                result={
                    'redirect_url': url_for('admin.index')
                }
            )
        else:
            user = User.get_by_login_name(login_name)
            if user is None:
                return fail(message=u'用户不存在')
            return fail(
                message=u'用户名或密码错误，请重新登陆'
            )

    if form.errors:
        return fail(
            result={
                'error': True,
                'messages': form.errors
            }
        )
    return render_template('admin/account/login.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def sign_up():
    pass


@bp.route("/logout", methods=['POST'])
@rbac.allow(['anonymous'], ['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('account.sign_in'))


@bp.route("/detail", methods=['GET', 'POST'])
@rbac.allow(['superuser', 'manager'], methods=['GET', 'POST'])
@login_required
def profile():
    pass
