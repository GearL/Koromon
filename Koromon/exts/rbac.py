from flask_login import current_user
from flask_rbac import RBAC

from Koromon.account.models import User, Role

rbac = RBAC()


def setup_rbac(app):
    rbac.init_app(app)
    rbac.set_role_model(Role)
    rbac.set_user_model(User)
    rbac.set_user_loader(lambda *args: current_user)
