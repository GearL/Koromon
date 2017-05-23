# -*- coding: utf-8 -*-

from __future__ import absolute_import

from envcfg.raw import koromon
from flask import Flask
from flask import render_template

from koromon.account.views import bp as account_bp
from koromon.article.views import bp as article_bp
from koromon.exts import db
from koromon.exts import setup_login_manager
from koromon.exts import setup_rbac


def create_app(name=None, config=None):
    app = Flask(name or __name__)

    app.config.from_object('envcfg.raw.koromon')

    app.debug = bool(int(koromon.DEBUG))
    app.config['TESTING'] = bool(int(koromon.TESTING))

    db.init_app(app)
    setup_login_manager(app)
    setup_rbac(app)
    setup_error_pages(app)

    app.register_blueprint(account_bp)
    app.register_blueprint(article_bp)

    return app


def setup_error_pages(app):
    @app.errorhandler(403)
    def page_not_found(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def method_not_allow(error):
        return render_template('errors/405.html'), 405
