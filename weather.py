from homeassistant.helpers.entity import Entity
import os, json, logging, time, requests
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([WeatherEntity(config)])

class WeatherEntity(Entity):
    def __init__(self, config):
        self._state = ''
        self._attributes = {
            'data_path': config['data_path'],
            'last_checked': 0,
            'frequency': config['frequency'],
            'api_key': config['API_key'],
            'location_key': config['location_key'],
            'temperature': 0,
            'temperature_unit': '',
            'condition': self._state,
            'pressure': 0,
            'humidity': 0,
            'ozone': 0,
            'visibility': 0,
            'wind_speed': 0,
            'wind_bearing': 0,
            'forecast': [],
            'attribution': '',
        }
        self.get_states()

    @property
    def device_state_attributes(self):
        return self._attributes

    @property
    def name(self) -> str:
        return 'Haccuweather'

    @property
    def state(self) -> str:
        return self._state

    def update(self):
        current_time = time.time()
        if (current_time - self._attributes['last_checked']) > self._attributes['frequency']: self.call_api()
        self.get_states()

    ## data_file_exists(file_state) - Checks if file_state or file exists in the data path.
    def data_file_exists(self, file_state) -> bool:
        return os.path.exists(os.path.join(self._attributes['data_path'], file_state))

    ## get_states() - Parses the data from the data files into the entity elements.
    def get_states(self):
        current = {}
        forecast = {}
        if self.data_file_exists('current.json'):
            with open(os.path.join(self._attributes['data_path'], 'current.json'), 'r') as f:
                current = json.load(f)[0]
            f.close()
        if self.data_file_exists('forecast.json'):
            with open(os.path.join(self._attributes['data_path'], 'forecast.json'), 'r') as f:
                forecast = json.load(f)["DailyForecasts"]
            f.close()
            parsed_forecast = self.parse_forecast(forecast)

        try:    
            self._state = current['WeatherText']
            self._attributes['last_checked'] = current['EpochTime']
            self._attributes['temperature'] = current['Temperature']['Imperial']['Value']
            self._attributes['temperature_unit'] = current['Temperature']['Imperial']['Unit']
            self._attributes['condition'] = self._state
            self._attributes['pressure'] = current['Pressure']['Imperial']['Value']
            self._attributes['humidity'] = current['RelativeHumidity']
            #self._attributes['ozone'] = 0
            self._attributes['visibility'] = current['Visibility']['Imperial']['Value']
            self._attributes['wind_speed'] = current['Wind']['Speed']['Imperial']['Value']
            self._attributes['wind_bearing'] = current['Wind']['Direction']['Degrees']
            if parsed_forecast is not None: self._attributes['forecast'] = parsed_forecast
            self._attributes['attribution'] = current["Link"]
        except:
            _LOGGER.error("Could not read data from file. Please check the data path.")

    ## call_api() - Submits request to AccuWeather API & stores response as JSON in configured path.
    def call_api(self):
        current = requests.get(f'http://dataservice.accuweather.com/currentconditions/v1/{self._attributes["location_key"]}?apikey={self._attributes["api_key"]}&details=true')
        with open(os.path.join(self._attributes['data_path'], 'current.json'), 'w') as f:
            f.write(current.text)
        f.close()
        forecast = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{self._attributes["location_key"]}?apikey={self._attributes["api_key"]}&details=true')
        with open(os.path.join(self._attributes['data_path'], 'forecast.json'), 'w') as f:
            f.write(forecast.text)
        f.close()

    ## parse_forecast(days) - Parse JSON data from forecast data file into list.
    def parse_forecast(self, days):
        forecast = []
        for day in days:
            if datetime.now().hour < 12: time_flag = "Day"
            else: time_flag = "Night"

            day_dict = {
                "datetime": day["Date"],
                "temperature": day["Temperature"]["Maximum"]["Value"],
                "condition": day[time_flag]["IconPhrase"],
                "templow": day["Temperature"]["Minimum"]["Value"],
                "precipitation": day[time_flag]["TotalLiquid"]["Value"],
                "precipitation_probability": day[time_flag]["PrecipitationProbability"],
                "wind_bearing": day[time_flag]["Wind"]["Direction"]["Degrees"],
                "wind_speed": day[time_flag]["Wind"]["Speed"]["Value"]
            }

            forecast.append(day_dict)
        return forecast
