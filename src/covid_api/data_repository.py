import csv
import io
import json
import os
from datetime import datetime
from jsonpickle import encode
from math import isnan
from pathlib import Path
from operator import itemgetter

import pandas as pd
import requests

from . import cache

TIME_SERIES_STATE_URL = "https://covidtracking.com/api/v1/states/daily.json"
TIME_SERIES_US_CASES_COUNTY_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
LOCALE_DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv"

class FIPSMerge(object):
    """A record of several locales that are merged in the NYT dataset.
    
    These are assigned a "fake FIPS" ID so they don't have to be treated specially outside this module.
    Real FIPS IDs are limited to 5 digits so the fake ones will started at 100,000.
    """

    def __init__(self, fake_id, real_ids, key_id, county, state, disclaimer):
        """Construct a new FIPSMerge.

        Args:
            fake_id (int): The assigned fake FIPS id.
            real_ids ([int]): The read IDs that are grouped.
            key_id (int): The real ID that the locale data should use.
            county (string): The county name used in the NYT dataset.
            state (string): The full state name used in the NYT dataset.
            disclaimer (string): An explanation of the merge for the user.
        """
        self.fake_id = fake_id
        self.real_ids = real_ids
        self.key_id = key_id
        self.county = county
        self.state = state
        self.disclaimer = disclaimer

MERGED_FIPS = [
    FIPSMerge(100_000, [36047, 36061, 36081, 36005, 36085], 36061, "New York City", "New York", 
        "All cases for the five boroughs of New York City (New York, Kings, Queens, Bronx and Richmond counties) are assigned to a single area called New York City."),
]

def smooth(self):
    return self.rolling(7, center=True).mean()
pd.Series.smooth = smooth
del smooth

@cache.memoize(timeout=86400)
def get_state_info():
    counter = 0
    def transform_state(key, value):
        nonlocal counter
        counter += 1
        return {
            "id": counter,
            "name": value["StateFull"],
            "abbrev": key,
            "population": value["2019"],
        }

    script_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = str(Path(script_path) / 'static-data/state-population-est2019.csv')

    state_populations = pd.read_csv(csv_path, index_col='State', usecols=['State', 'StateFull', '2019'], keep_default_na=False, thousands=',', sep=',', engine='python')
    state_populations["2019"] = state_populations["2019"].astype('int')

    state_dict = state_populations.to_dict(orient='index')
    return [transform_state(key, value) for key, value in state_dict.items()]

@cache.memoize(timeout=86400)
def get_locale_info() -> pd.DataFrame:
    locale_data_csv = requests.get(LOCALE_DATA_URL).text
    locale_data = pd.read_csv(io.StringIO(locale_data_csv), index_col='FIPS')

    for fips_merge in MERGED_FIPS:
        merged_population = 0
        locale_data.loc[fips_merge.fake_id] = locale_data.loc[fips_merge.key_id]

        for real_id in fips_merge.real_ids:
            merged_population += locale_data.loc[real_id, 'Population']
            locale_data.drop(real_id, inplace=True)

        locale_data.loc[fips_merge.fake_id, 'Population'] = merged_population

    return locale_data

@cache.memoize(timeout=3600)
def get_state_level_data() -> pd.DataFrame:
    data = requests.get(TIME_SERIES_STATE_URL).json()
    for record in data:
        record["date"] = datetime.strptime(str(record["date"]), "%Y%m%d")

    return pd.DataFrame(data).set_index('date')

@cache.memoize(timeout=3600)
def get_grouped_county_data() -> pd.DataFrame:
    county_case_data = pd.read_csv(io.StringIO(requests.get(TIME_SERIES_US_CASES_COUNTY_URL).text), index_col='date')
    county_case_data.index = pd.to_datetime(county_case_data.index)

    for fips_merge in MERGED_FIPS:
        county_case_data.loc[(county_case_data['county'] == fips_merge.county) &
                         (county_case_data['state'] == fips_merge.state), 'fips'] = fips_merge.fake_id

    return county_case_data.groupby('fips')

def get_empty_dataframe(start_time: datetime, end_time: datetime) -> pd.DataFrame:
    return pd.DataFrame(index=pd.date_range(start_time, end_time))

class Locale(object):
    population = 0
    name = ""

class RequestCache(object):
    def __init__(self):
        self.grouped_county_data = get_grouped_county_data()
        self.locale_info = get_locale_info()
        self.state_info = get_state_info()
        self.grouped_state_data = get_state_level_data().groupby('state')

class Data(object):
    def __init__(self, start_time: datetime, end_time: datetime):
        super().__init__()
        self.deaths = get_empty_dataframe(start_time, end_time)
        self.hospitalized = get_empty_dataframe(start_time, end_time)
        self.positive = get_empty_dataframe(start_time, end_time)
        self.positiveRate = get_empty_dataframe(start_time, end_time)
        self.locales = []
        self.request_cache = RequestCache()

    def _roundtrip(self, obj: pd.DataFrame):
        return json.loads(obj.to_json())

    def _process_type(self, obj: pd.DataFrame):
        data = self._roundtrip(obj)
        for locale in self.locales:
            if locale.name not in data:
                data[locale.name] = {}
            
            data[locale.name] = { k: v for k, v in data[locale.name].items() if v != None }
        
        return data

    def to_json(self):
        data = {
            "deaths" : self._process_type(self.deaths),
            "hospitalized": self._process_type(self.hospitalized),
            "positive": self._process_type(self.positive),
            "positiveRate": self._process_type(self.positiveRate),
            "locales": [locale.__dict__ for locale in self.locales],
        }

        return json.dumps(data)
        
class DataRepository(object):
    def get_empty_data_object(self, start_time: datetime, end_time: datetime) -> Data:
        return Data(start_time, end_time)
    
    def add_county_data(self, data: Data, fips):
        county_data = data.request_cache.grouped_county_data.get_group(fips)
        locale_info = data.request_cache.locale_info.loc[fips]

        locale = Locale()
        locale.population = int(locale_info["Population"])
        locale.name = locale_info["Combined_Key"]

        data.locales.append(locale)
        data.deaths[locale.name] = county_data["deaths"].diff().smooth()
        data.positive[locale.name] = county_data["cases"].diff().smooth()

    def add_state_data(self, data: Data, state_id):
        state_info = data.request_cache.state_info[state_id - 1]
        state_abbrev = state_info['abbrev']
        state_data = data.request_cache.grouped_state_data.get_group(state_abbrev)

        locale = Locale()
        locale.population = int(state_info['population'])
        locale.name = state_abbrev

        data.locales.append(locale)
        data.deaths[state_abbrev] = state_data["deathIncrease"].smooth()
        data.hospitalized[state_abbrev] = state_data["hospitalizedCurrently"].smooth()
        data.positive[state_abbrev] = state_data["positiveIncrease"].smooth()
        data.positiveRate[state_abbrev] = ((state_data["positiveIncrease"] * 100) / state_data["totalTestResultsIncrease"]).smooth()

    def _get_valid_locales(self):
        locale_info = get_locale_info()
        return locale_info[locale_info.index.notnull()]

    def get_available_locales(self):
        return self._get_valid_locales().to_dict(orient='index')

    def get_state_data(self):
        return get_state_info()

    def get_available_locales_for_state(self, state_abbrev):
        def transform_locale(key, value):
            merge = next((merge for merge in MERGED_FIPS if merge.fake_id == key), None)
            disclaimer = merge.disclaimer if merge != None else ''

            return {
                "id": int(key),
                "name": value["Admin2"],
                "full_name": value['Combined_Key'],
                "population": value['Population'],
                "disclaimer": disclaimer,
            }


        state = next(filter(lambda s: s['abbrev'] == state_abbrev, self.get_state_data()))['name']
        locales = self._get_valid_locales()
        filtered_locales = locales[(locales['Province_State'] == state) &
                                   (locales['Admin2']) &
                                   (locales["Lat"])].to_dict(orient='index')
        return sorted([transform_locale(fips, locale) for fips, locale in filtered_locales.items()], key=itemgetter('name'))
    
