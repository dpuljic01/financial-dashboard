from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.decorators import check_confirmed
from server.models import User

bp = Blueprint("profile", __name__, url_prefix="/api/users/self")


@bp.route("", methods=["GET"])
@jwt_required
@check_confirmed  # this absolutely **must** come after @jwt_required decorator
def get_user():
    current_identity = get_jwt_identity()
    user = User.query.get_or_404(current_identity)
    return jsonify(user.json)
