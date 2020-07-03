from simplejson import dumps
from flask.wrappers import Response

def _make_response(json):
    return Response(response=json,
                status=200,
                mimetype="application/json") 

def preencoded_json(func):
    def func_wrapper(*args, **kwargs):
        return _make_response(func(*args, **kwargs))
    return func_wrapper

def customize_json(*args, **kwargs):
    def decorate(func):
        def func_wrapper(*inner_args, **inner_kwargs):
            return _make_response(dumps(func(*inner_args, **inner_kwargs), *args, **kwargs))
        return func_wrapper
    return decorate

def json_api_doc(func):
    def func_wrapper(*args, **kwargs):
        return { "data": func(*args, **kwargs) }
    return func_wrapper