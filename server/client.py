""" Client App """
import os
from flask import Blueprint, current_app, send_file, send_from_directory
import requests

client_bp = Blueprint(
    'client_app', __name__,
    url_prefix='',
    static_url_path='',
    static_folder='./../dist/static/',
    template_folder='./../dist/',
)

print("BLAAA")

@client_bp.route("/<string:path>")
def catch_all(path):
    print("PAATJH: ", path)
    dist_dir = current_app.config['DIST_DIR']
    if path != "" and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(os.path.join(dist_dir), path)
    return send_from_directory(os.path.join(dist_dir), "index.html")
