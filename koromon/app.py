# -*- coding: utf-8 -*-

from __future__ import absolute_import

from envcfg.raw import koromon
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from koromon.admin.views.main import bp as admin_bp
from koromon.account.views import bp as account_bp
from koromon.article.views import bp as article_bp
from koromon.pages.views import views as pages_bp
from koromon.exts.database import db
from koromon.exts.login_manager import setup_login_manager
from koromon.exts.rbac import setup_rbac
from koromon.utils.resp import is_setup


def create_app(name=None, config=None):
    app = Flask(name or __name__)

    app.config.from_object('envcfg.raw.koromon')

    app.debug = bool(int(koromon.DEBUG))
    app.config['TESTING'] = bool(int(koromon.TESTING))

    db.init_app(app)
    setup_login_manager(app)
    setup_rbac(app)
    setup_error_pages(app)
    setup_redirect_page(app)

    app.register_blueprint(admin_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(pages_bp)

    return app


def setup_redirect_page(app):
    @app.before_request
    def redirect_setup():
        if not is_setup() and request.path != "/setup":
            return redirect(url_for('pages.setup'))


def setup_error_pages(app):
    @app.errorhandler(403)
    def page_not_found403(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found404(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def method_not_allow405(error):
        return render_template('errors/405.html'), 405
