from flask import Blueprint
from flask_cors import cross_origin

mainRoute = Blueprint('main', __name__)


@mainRoute.route('/')
@cross_origin(supports_credentials=True)
def index():
    return "<h1>API used for a FullStack Challenge in Python and React<h1>"
