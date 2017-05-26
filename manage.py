from flask_script import Manager
from setuptools import find_packages

from koromon.app import create_app
from koromon.exts.database import db

application = create_app('koromon')
manager = Manager(application)


def _import_models():
    koromon_packages = find_packages('./koromon')
    for each in koromon_packages:
        guess_module_name = 'koromon.%s.models' % each
        try:
            __import__(guess_module_name, globals(), locals())
            print 'Find model:', guess_module_name
        except ImportError:
            pass


@manager.command
def syncdb():
    with application.test_request_context():
        _import_models()
        db.create_all()
        db.session.commit()
    print 'Database Created'


@manager.command
def dropdb():
    with application.test_request_context():
        db.drop_all()
    print 'Database Dropped'


if __name__ == '__main__':
    manager.run()
