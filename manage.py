from flask_script import Manager, Server

from Koromon.app import create_app


application = create_app()
manager = Manager(application)


if __name__ == '__main__':
    manager.run()

