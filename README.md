# haccuweather

A custom entity modification of the AccuWeather integration in Home Assistant.

This is a WIP for use with the default or any supported weather card in Home Assistant or HACS. It creates an entity that can be used anywhere entities are supported in Home Assistant.

This custom component was created in an attempt to leverage the limited (free) API plan offered by AccuWeather. At the time of writing, the limited (free) plan offers a maximum of 50 calls/day. The provided Home Assistant integration for AccuWeather was exceeding the alotted number of calls in a day. This component calls the API once per hour for current conditions and the forecast. The frequencies can be adjusted manually if desired. (An option to make it configurable may make it to future updates if there is a demand for it.)

---
## Installation
1. Clone or download the repository into your `config/custom_components` directory.

2. Add the following to your `configuration.yaml` file.

    ```yaml
    weather:
      - platform: haccuweather
        data_path: </path/to/json/data/folder> #example: /home/homeassistant/.homeassitant/custom_components/haccuweather/data
        API_key: <your_AccuWeather_API_key>
        location_key: <your_AccuWeather_location_key>
    ```

    The `data_path` must be writable by the user running Home Assistant. The script that fetches the data from the [AccuWeather API](https://developer.accuweather.com/) will write two files into this directory (`current.json` & `forecast.json`). These two files will contain the responses from CURL using the `location_key` & your `API_key`. See the [AccuWeather API](https://developer.accuweather.com/) reference page for obtaining an [API key](https://developer.accuweather.com/user/me/apps) and [location key](https://developer.accuweather.com/accuweather-locations-api/apis).

<span style="color:red; font-size: 0.7em;">3. WIP [setup cron task to run updater for Accuweather API]</span>

<span style="color:red; font-size: 0.7em;">4. WIP [restart hass]</span>
