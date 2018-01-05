from flask import Flask, request, jsonify, Blueprint, abort
from openvasup.omp import NotFoundError

class BaseAPI:
    version = 1
    model = None

    def __init__(self, model, entity=None):
        self.model = model
        self.entity = model.get_entity() if entity is None else entity

    def respond(self, data=None):
      if isinstance(data, list):
        return jsonify(results=data)
      
      return jsonify(data)

    def create(self):
        """ Create an new instance of the entity """
        data = request.get_json(silent=True)
        obj = self.model.from_dict(data)
        obj.save()
        return self.respond(obj.to_dict())
      
    def search(self):
        """ Get all the results for an entity """
        query = request.args.to_dict()
        # @todo handle sorting
        # @todo take filter_id
        if 'page' in query:
            query['first'] = query['page']
            del query['page']
        
        if 'filter' in query:
            query['@filter'] = query['filter']
            del query['filter']
        else:
            query = {'@filter': query}
        return self.respond([d.to_json() for d in self.model.get(query)])
      
    def get(self, uuid):
        """ Get a specific entity of the provided uuid """         
        try:
            result = self.model.get_by_id(uuid)
        except NotFoundError:
            return abort(404)

        if result is None:
            return abort(404)
        return self.respond(result.to_json())

    def update(self, uuid):
        """ Update a specific entity of the provided uuid """
        data = request.get_json(silent=True)
        try:
            result = self.model.get_by_id(uuid)
        except NotFoundError:
            return abort(404)
        for k in data:
            setattr(obj, k, data[k])
        obj.save()
        return self.respond(obj.to_json())

    def delete(self, uuid):
        """ Delete a specific entity of the provided uuid """
        try:
            ultimate = int(request.args.get('ultimate', False))
        except:
            ultimate = False
        obj = self.model.from_dict({'@id': uuid})
        req = obj.delete(ultimate)
        return self.respond({'success': True})

    def register(self, app):
      entity = self.entity.replace('_', '-')
      app.add_url_rule('/%s' % entity, view_func=self.create, methods=['POST'])
      app.add_url_rule('/%s' % entity, view_func=self.search, methods=['GET'])
      app.add_url_rule('/%s/<uuid>' % entity, view_func=self.get, methods=['GET'])
      app.add_url_rule('/%s/<uuid>' % entity, view_func=self.update,  methods=['POST'])
      app.add_url_rule('/%s/<uuid>' % entity, view_func=self.delete, methods=['DELETE'])
      return app