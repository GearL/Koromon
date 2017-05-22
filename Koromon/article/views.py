from flask import Blueprint

from Koromon.exts import rbac

bp = Blueprint('article', __name__, url_prefix='/article')


@bp.route('/<string:category>/list', methods=['GET'])
@rbac.allow(['anonymous'], methods=['GET'])
def all_list(category):
    pass
