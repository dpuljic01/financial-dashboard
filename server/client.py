""" Client App """
import os
from flask import Blueprint, current_app, send_from_directory
from server.decorators import gzipped

client_bp = Blueprint("client_app", __name__, template_folder='./../dist')


@client_bp.route("/", defaults={"path": ""})
@client_bp.route("/<path:path>")
def catch_all(path):
    dist_dir = current_app.config["DIST_DIR"]
    if path != "" and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(os.path.join(dist_dir), path)
    return send_from_directory(os.path.join(dist_dir), "index.html")
