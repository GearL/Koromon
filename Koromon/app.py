# -*- coding: utf-8 -*-

from __future__ import absolute_import

from envcfg.raw import koromon
from flask import Flask

from Koromon.account.views import bp as account_bp
from Koromon.article.views import bp as article_bp
from Koromon.exts import setup_database, setup_login_manager
from Koromon.exts import setup_rbac


def create_app(name=None, config=None):
    app = Flask(name or __name__)

    app.config.from_object('envcfg.raw.koromon')

    app.debug = bool(int(koromon.DEBUG))
    app.config['TESTING'] = bool(int(koromon.TESTING))

    setup_database(app)
    setup_login_manager(app)
    setup_rbac(app)

    app.register_blueprint(account_bp)
    app.register_blueprint(article_bp)

    return app
