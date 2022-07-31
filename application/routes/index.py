from flask import Blueprint

mainRoute = Blueprint('main', __name__)


@mainRoute.route('/')
def index():
    return "<h1>API used for a FullStack Challenge in Python and React<h1>"
