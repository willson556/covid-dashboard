from datetime import datetime

from flask import jsonify, Response
from flask_restful import Resource
from marshmallow.validate import Regexp
from webargs import fields
from webargs.flaskparser import use_args

from .data_repository import DataRepository
from .util.api_decorators import customize_json, preencoded_json, json_api_doc
from . import api, cache

repository = DataRepository()

get_data_args = {
    'start_time': fields.DateTime(format='%Y-%m-%d'),
    'end_time': fields.DateTime(format='%Y-%m-%d'),
    'states': fields.List(fields.Str()),
    'fips': fields.List(fields.Int()),
}

class DataEndpoint(Resource):
    @preencoded_json
    @use_args(get_data_args, location='query')
    def get(self, args):
        data = repository.get_empty_data_object(args['start_time'], args['end_time'])

        if 'states' in args:
            for state in args['states']:
                repository.add_state_data(data, state)
        
        if 'fips' in args:
            for locale in args['fips']:
                repository.add_county_data(data, locale)
        return data.to_json()

class StateEndpoint(Resource):
    def add_county_link(self, state):
        state["links"] = { "counties": "/api/counties_for_state?state=" + state["abbrev"] }
        return state

    def get(self):
        return {"states":  [self.add_county_link(state) for state in repository.get_state_data()] }

class CountyEndpoint(Resource):
    @customize_json(ignore_nan=True)
    def get(self):
        return repository.get_available_locales()

class CountiesForStateEndpoint(Resource):
    @use_args({'state': fields.Str(validate=Regexp(r"[A-Z]{2}"))}, location='query')
    @customize_json(ignore_nan=True)
    def get(self, args):
        return {"counties" : repository.get_available_locales_for_state(args['state']) }

