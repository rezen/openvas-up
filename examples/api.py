from __future__ import print_function
import pprint
import sys
sys.path.append("..")
from openvasup.omp import NotFoundError
from openvasup.model import OpenvasObject
from openvasup.api.base import BaseAPI
from openvasup.api.task import TaskAPI
from openvasup.meta import Tag
from openvasup.scan import Task, Report, Result, Note
from openvasup.config import Alert, Credential, Config, Setting
from openvasup.asset import Asset, Target, PortList
from flask import Flask, Blueprint, jsonify, g
import time

def add_common_routes(app):
    @app.before_request
    def before_request():
        g.start = time.time()
    
    @app.after_request
    def after_request(response):
        diff = time.time() - g.start
        response.headers.add('X-Timing', diff)
        return response

    @app.errorhandler(404)
    @app.errorhandler(NotFoundError)
    def page_not_found(e):
        response = jsonify(success=False, message="Not Found")
        response.status_code = 404
        return response

    @app.route("/")
    def home():
        return jsonify(version=1.0)

    return app

def add_model_routes(app):
    models = [PortList, Asset, Target, Setting, Config, Alert, Report, Result, Note, Tag]
    bp = Blueprint('tasks', __name__)
    api = TaskAPI(Task)
    bp = api.register(bp) 
    app.register_blueprint(bp, url_prefix='/v%s' % TaskAPI.version)

    for model in models:
        bp = Blueprint(model.get_entity(), __name__)
        api = BaseAPI(model)
        bp = api.register(bp)
        app.register_blueprint(bp, url_prefix='/v%s' % BaseAPI.version)
    return app

def add_routes(app):
    app = add_common_routes(app)
    add = add_model_routes(app)
    return app

def main():
    username = 'admin'
    password = 'admin'
    OpenvasObject.connect(username=username, password=password, host='192.168.99.100')
    pp = pprint.PrettyPrinter(indent=2)
    app = Flask(__name__)
    app = add_routes(app)
    app.run(port=5002) 

if __name__ == "__main__":
    main()
