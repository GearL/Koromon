# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Flask, current_app
from envcfg.raw import Koromon

from Koromon.exts import db, setup_database, setup_login_manager
from Koromon.exts import setup_rbac
from Koromon.account.views import bp as account_bp
from Koromon.article.views import bp as article_bp


def create_app(name=None, config=None):

    app = Flask(name or __name__)

    app.config.from_object('envcfg.raw.Koromon')

    app.debug = bool(int(Koromon.DEBUG))
    app.config['TESTING'] = bool(int(Koromon.TESTING))

    setup_database(app)
    setup_login_manager(app)
    setup_rbac(app)

    app.register_blueprint(account_bp)
    app.register_blueprint(article_bp)


    return app

