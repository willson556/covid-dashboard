import cProfile
from datetime import datetime
from covid_api.api import DataEndpoint

endpoint = DataEndpoint()

def run():
    endpoint.get({
        'start_time': datetime(2020, 3, 1),
        'end_time': datetime(2020, 7, 12),
        'states': [5],
        'counties': [6001, 6085, 6087, 6081, 6041, 6013],
    })

run()
cProfile.run('run()', 'stats2')