"""A custom entity modification of the AccuWeather integration in Home Assistant."""
from . import weather

DOMAIN = 'haccuweather'

def setup(hass, config):
    def call_api(call):
        weather._LOGGER.info("Haccuweather is calling API manually/forcefully ...")
        weather.haccuweather_entity.call_api()

    hass.services.register(DOMAIN, 'call_api', call_api)
    return True
