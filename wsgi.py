# -*- coding: utf-8 -*-

from werkzeug.contrib.fixers import ProxyFix

from koromon.app import create_app

application = create_app('koromon')

application.wsgi_app = ProxyFix(application.wsgi_app)
