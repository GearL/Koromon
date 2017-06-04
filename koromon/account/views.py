# coding=utf-8
from flask import Blueprint, redirect, url_for
from flask import render_template, request
from flask_login import current_user, login_user
from flask_login import login_required, logout_user

from koromon.account.forms import SignInForm, SignUpForm
from koromon.account.models import User, Role
from koromon.exts.rbac import rbac
from koromon.utils.resp import fail, success

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/sign_in', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], methods=['GET', 'POST'])
def sign_in():
    if not current_user.is_anonymous():
        return redirect(url_for('admin_main.index'))

    form = SignInForm()

    if form.validate_on_submit():
        login_name = request.form['login_name'].strip()
        password = request.form['password'].strip()
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
                    'redirect_url': url_for('admin_main.index')
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


@bp.route('/sign_up', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def sign_up():
    if not current_user.is_anonymous():
        return redirect(url_for('admin_main.index'))

    form = SignUpForm()

    if form.validate_on_submit():
        login_name = request.form['login_name'].strip()
        password = request.form['password'].strip()
        nickname = request.form['nickname']

        user = User.get_by_login_name(login_name)
        if user is not None:
            return User.check_login_name(login_name)

        normal = Role.get_by_name('normal')
        user = User(
            login_name=login_name,
            nickname=nickname,
            password=password
        )
        user.roles.append(normal)
        user.role_id = normal.id
        user.state = 'unactivated'
        user.save()
        return success(
            result={
                'redirect_url': url_for('pages.static_html')
            }
        )

    if form.errors:
        return fail(
            result={
                'errors': True,
                'messages': form.errors
            }
        )
    return render_template('admin/account/signup.html', form=form)


@bp.route('/sign_out', methods=['POST'])
@rbac.allow(['anonymous'], ['POST'])
@login_required
def sign_out():
    logout_user()
    return success(
        result={
            'redirect_url': url_for('account.sign_in')
        }
    )


@bp.route('/profile', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def get_profile():
    user = User.get_by_login_name(current_user.login_name)
    return render_template('admin/account/profile.html', user=user)


@bp.route('/profile', methods=['PATCH'])
@rbac.allow(['superuser', 'manager'], methods=['PATCH'])
@login_required
def update_profile():
    user = User.get_by_login_name(current_user.login_name)
    user.update(request.form)
    return success(message=u'更新成功')
