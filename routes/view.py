from flask import Blueprint, send_from_directory, send_file

view_bp = Blueprint("view", __name__)


@view_bp.route("/")
def view_index():
    return send_file("view/dist/index.html")


@view_bp.route("/<path:path>")
def view(path):
    return send_from_directory("view/dist", path)
