from datetime import datetime

from flask import jsonify, Response
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from .data_repository import DataRepository
from . import api, cache

repository = DataRepository()

get_data_args = {
    'start_time': fields.DateTime(format='%Y-%m-%d'),
    'end_time': fields.DateTime(format='%Y-%m-%d'),
    'states': fields.List(fields.Str()),
    'fips': fields.List(fields.Int()),
}

class DataEndpoint(Resource):
    @use_args(get_data_args, location='query')
    def get(self, args):
        data = repository.get_empty_data_object(args['start_time'], args['end_time'])

        if 'states' in args:
            for state in args['states']:
                repository.add_state_data(data, state)
        
        if 'fips' in args:
            for locale in args['fips']:
                repository.add_county_data(data, locale)

        return Response(response=data.to_json(),
                        status=200,
                        mimetype="application/json") 

class StateEndpoint(Resource):
    def get(self):
        return repository.get_available_states()

class CountyEndpoint(Resource):
    def get(self):
        return repository.get_available_locales()

