from homeassistant.helpers.entity import Entity
import os, json, logging

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([WeatherEntity(config)])

class WeatherEntity(Entity):
    def __init__(self, config):
        self._state = ''
        self._attributes = {
            'data_path': config['data_path'],
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
        #_LOGGER.info("Haccuweather is running an update ...")
        #TODO Check time schedule and reach out to API
        self.get_states()

    def data_file_exists(self, file_state) -> bool:
        return os.path.exists(os.path.join(self._attributes['data_path'], file_state))

    def get_states(self):
        current = {}
        forecast = {}
        if self.data_file_exists('current.json'):
            with open(os.path.join(self._attributes['data_path'], 'current.json'), 'r') as f:
                current = json.load(f)[0]
            f.close()
        if self.data_file_exists('forecast.json'):
            with open(os.path.join(self._attributes['data_path'], 'forecast.json'), 'r') as f:
                forecast = json.load(f)
            f.close()
            
        self._state = current['WeatherText']
        self._attributes['temperature'] = current['Temperature']['Imperial']['Value']
        self._attributes['temperature_unit'] = current['Temperature']['Imperial']['Unit']
        self._attributes['condition'] = self._state
        self._attributes['pressure'] = current['Pressure']['Imperial']['Value']
        self._attributes['humidity'] = current['RelativeHumidity']
        #self._attributes['ozone'] = 0
        self._attributes['visibility'] = current['Visibility']['Imperial']['Value']
        self._attributes['wind_speed'] = current['Wind']['Speed']['Imperial']['Value']
        self._attributes['wind_bearing'] = current['Wind']['Direction']['Degrees']
        #self._attributes['forecast'] = []
        self._attributes['attribution'] = current["Link"]
