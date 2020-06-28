import csv
import io
import json
from datetime import datetime
from jsonpickle import encode

import pandas as pd
import requests

from . import cache

TIME_SERIES_STATE_URL = "https://covidtracking.com/api/v1/states/daily.json"
TIME_SERIES_US_CASES_COUNTY_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
LOCALE_DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv"


def smooth(self):
    return self.rolling(7, center=True).mean()
pd.Series.smooth = smooth
del smooth

@cache.memoize(timeout=3600)
def get_state_level_data() -> pd.DataFrame:
    data = requests.get(TIME_SERIES_STATE_URL).json()
    for record in data:
        record["date"] = datetime.strptime(str(record["date"]), "%Y%m%d")

    return pd.DataFrame(data).set_index('date')

@cache.memoize(timeout=86400)
def get_state_populations() -> pd.DataFrame:
    state_populations = pd.read_csv("src/covid_api/static-data/state-population-est2019.csv", index_col='State', usecols=['State', '2019'], keep_default_na=False, thousands=',', sep=',', engine='python')
    state_populations["2019"] = state_populations["2019"].astype('int')
    return state_populations

@cache.memoize(timeout=86400)
def get_locale_info() -> pd.DataFrame:
    locale_data_csv = requests.get(LOCALE_DATA_URL).text
    locale_data = pd.read_csv(io.StringIO(locale_data_csv), index_col='FIPS')
    return locale_data

@cache.memoize(timeout=3600)
def get_county_level_data() -> pd.DataFrame:
    county_case_data = pd.read_csv(io.StringIO(requests.get(TIME_SERIES_US_CASES_COUNTY_URL).text), index_col='date')
    county_case_data.index = pd.to_datetime(county_case_data.index)
    return county_case_data

@cache.memoize(timeout=60)
def get_grouped_county_data():
    return get_county_level_data().groupby('fips')

def get_empty_dataframe(start_time: datetime, end_time: datetime) -> pd.DataFrame:
    return pd.DataFrame(index=pd.date_range(start_time, end_time))

class Locale(object):
    population = 0
    name = ""

class Data(object):
    def __init__(self, start_time: datetime, end_time: datetime):
        super().__init__()
        self.deaths = get_empty_dataframe(start_time, end_time)
        self.hospitalized = get_empty_dataframe(start_time, end_time)
        self.positive = get_empty_dataframe(start_time, end_time)
        self.tests = get_empty_dataframe(start_time, end_time)
        self.locales = []

    def _roundtrip(self, obj: pd.DataFrame):
        return json.loads(obj.to_json())

    def to_json(self):
        data = {
            "deaths" : self._roundtrip(self.deaths),
            "hospitalized": self._roundtrip(self.hospitalized),
            "positive": self._roundtrip(self.positive),
            "tests": self._roundtrip(self.tests),
            "locales": [locale.__dict__ for locale in self.locales],
        }

        return json.dumps(data)
        
class DataRepository(object):
    def get_empty_data_object(self, start_time: datetime, end_time: datetime) -> Data:
        return Data(start_time, end_time)
    
    def add_county_data(self, data: Data, fips):
        county_data = get_grouped_county_data().get_group(fips)
        locale_info = get_locale_info().loc[fips]

        locale = Locale()
        locale.population = int(locale_info["Population"])
        locale.name = locale_info["Combined_Key"]

        data.locales.append(locale)
        data.deaths[locale.name] = county_data["deaths"].diff().smooth()
        data.positive[locale.name] = county_data["cases"].diff().smooth()

    def add_state_data(self, data: Data, state_abbrev):
        state_data = get_state_level_data().groupby('state').get_group(state_abbrev)

        locale = Locale()
        locale.population = int(get_state_populations().loc[state_abbrev, '2019'])
        locale.name = state_abbrev

        data.locales.append(locale)
        data.deaths[state_abbrev] = state_data["deathIncrease"].smooth()
        data.hospitalized[state_abbrev] = state_data["hospitalizedCurrently"].smooth()
        data.positive[state_abbrev] = state_data["positiveIncrease"].smooth()
        data.tests = state_data["totalTestResultsIncrease"].smooth()

    def get_available_states(self):
        return list(get_state_populations().index.values)

    def get_available_locales(self):
        locale_info = get_locale_info()
        return locale_info[locale_info.index.notnull()].to_dict(orient='index')
       