import sys, os
sys.path.insert(1, os.path.abspath(os.getcwd()) + '/application/routes')
import bcbRequest, index, ipcaRequest

from flask import Flask
from .extensions import mongo


def create_app():
    app = Flask(__name__)

    app.register_blueprint(bcbRequest.bcbRequestRoute)
    app.register_blueprint(index.mainRoute)
    app.register_blueprint(ipcaRequest.ipcaRequestRoute)

    return app
