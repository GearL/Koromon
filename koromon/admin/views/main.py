from flask import Blueprint, render_template
from flask_login import login_required

from koromon.exts.rbac import rbac
from .account import bp as account_bp
from .article import bp as article_bp
from .pages import bp as page_bp

bp = Blueprint('admin_main', __name__, url_prefix='/admin')


@bp.route('/index', methods=['GET'])
@bp.route('/', methods=['GET'])
@rbac.allow(['superuser', 'manager'], methods=['GET'])
@login_required
def index():
    return render_template('admin/index.html')


def setup_admin_blueprint(app):
    app.register_blueprint(bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(page_bp)
