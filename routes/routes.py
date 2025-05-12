# ---------------------------------------------------------------- #
# ------- These routes handle the UI for the application  -------- #
# ---------------------------------------------------------------- #
from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@routes.route('/docs', methods=['GET'])
def docs():
    return render_template("docs.html")