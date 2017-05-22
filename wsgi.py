# -*- coding: utf-8 -*-

from werkzeug.contrib.fixers import ProxyFix

from Koromon.app import create_app


application = create_app('Koromon')

application.wsgi_app = ProxyFix(application.wsgi_app)

