from flask import Flask, request, jsonify, Blueprint, abort
from openvasup.omp import NotFoundError, ResultError
from openvasup.scan import Task
from base import BaseAPI

class TaskAPI(BaseAPI):
    """ Give additional API routes for tasks """
    version = 1

    def move(self, uuid): pass

    def resume(self, uuid):
        """ Resume a task """
        obj = self.model.from_dict({'@id': uuid})
        try:
          obj.resume()
        except ResultError as err:
          pass
        return 'resume %s' % uuid

    def start(self, uuid):
        """ Start a task """
        obj = self.model.from_dict({'@id': uuid})
        try:
            obj.start()
        except ResultError as err:
            pass
        return 'start %s' % uuid

    def stop(self, uuid):
        """ Stop a task """
        obj = self.model.from_dict({'@id': uuid})
        try:
            obj.stop()
        except ResultError as err:
            pass
        return 'stop %s' % uuid

    def register(self, app):
        entity = self.entity.replace('_', '-')
        app.add_url_rule('/%s' % entity, view_func=self.create, methods=['POST'])
        app.add_url_rule('/%s' % entity, view_func=self.search, methods=['GET'])
        app.add_url_rule('/%s/<uuid>' % entity, view_func=self.get, methods=['GET'])
        app.add_url_rule('/%s/<uuid>' % entity, view_func=self.update, methods=['POST'])
        app.add_url_rule('/%s/<uuid>' % entity, view_func=self.delete, methods=['DELETE'])
        app.add_url_rule('/%s/<uuid>/resume' % entity, view_func=self.resume, methods=['POST'])
        app.add_url_rule('/%s/<uuid>/start' % entity, view_func=self.start, methods=['POST'])
        app.add_url_rule('/%s/<uuid>/stop' % entity, view_func=self.stop, methods=['POST'])
        return app
