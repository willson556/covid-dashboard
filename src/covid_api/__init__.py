from dotenv import load_dotenv
from flask import Flask, jsonify
from flask.templating import render_template
from flask_caching import Cache
from flask_restful import Api

cache = Cache()
api = None


from .api import DataEndpoint, StateEndpoint, CountyEndpoint, CountiesForStateEndpoint

load_dotenv()
app = Flask(__name__)
api = Api(app)
cache.init_app(app, config={'CACHE_TYPE': 'simple'})
api.add_resource(DataEndpoint, '/api/data')
api.add_resource(StateEndpoint, '/api/states')
api.add_resource(CountyEndpoint, "/api/counties")
api.add_resource(CountiesForStateEndpoint, "/api/counties_for_state")

@app.errorhandler(400)
@app.errorhandler(422)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])

    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

@app.route('/')
def main_page():
    return render_template('index.html')
