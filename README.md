# haccuweather

A custom entity modification of the AccuWeather integration in Home Assistant.

This is a WIP for use with the default or any supported weather card in Home Assistant or HACS. It creates an entity that can be used anywhere entities are supported in Home Assistant.

This custom component was created in an attempt to leverage the limited (free) API plan offered by AccuWeather. At the time of writing, the limited (free) plan offers a maximum of 50 calls/day. The provided AccuWeather integration for Home Assistant was exceeding the alotted number of calls in a day. This component calls the API for current conditions and the forecast once per `frequency` from the last check. The `frequency` can be adjusted in the `configuration.yaml` file.

---

## Installation

1. Clone or download the repository into your `config/custom_components` directory. Name or rename the directory `haccuweather`. (So it should be `config/custom-components/haccuweather`)

2. Add the following to your `configuration.yaml` file.

    ```yaml
    weather:
      - platform: haccuweather
        data_path: </path/to/json/data/folder> #example: /home/homeassistant/.homeassitant/custom_components/haccuweather/data
        API_key: <your_AccuWeather_API_key>
        location_key: <your_AccuWeather_location_key>
        frequency: <time_in_seconds> #3600 (1 hour) is recommended for the limited plan
    haccuweather:
    ```

    The `data_path` must be writable by the user running Home Assistant. The script that fetches the data from the [AccuWeather API](https://developer.accuweather.com/) will write two files into this directory (`current.json` & `forecast.json`). These two files will contain the responses from Python requests using the `location_key` & your `API_key`. See the [AccuWeather API](https://developer.accuweather.com/) reference page for obtaining an [API key](https://developer.accuweather.com/user/me/apps) and [location key](https://developer.accuweather.com/accuweather-locations-api/apis).

    `frequency` is the number of seconds from the last check that the component should call the API.

3. Restart Home Assistant.

---

## Changelog

2021JAN11: Added custom service to call API manually/forecfully. See service `haccuweather.call_api` in developer tools or in available service calls in automations/scripts.

---

## Troubleshooting

> Icons aren't showing for certain conditions using HACS weather-card.

- The `weather-card.js` file in the `$config/www/community/weather-card` must be edited to include cases for the specific conditions. I've had the best luck opening the `weather-card.js.gz` archive, editing the `weather-card.js` file inside, saving & updating the archive, extracting the file to the directory overwriting the existing file and reloading the page. Of course, updates could kill this, so make a backup!

---

## For the Future

1. The plan is to reduce the frequency of forecast polling to a maximum of 4 times a day. It is my thought that a 5 day forecast doesn't need to be as up to date as the current conditions. This will allow for the current conditions to be updated more frequently than once per hour. This also opens up the possibility for weather alerts. For now, functionality for intermitent viewing is more important. I have found that a majority of the time, I check the weather on my phone using a dedicated app or widget. Home Assistant is more of a general information portal for the day's weather.

2. A translation file and/or icons would be a nice feature set for this component. Though, at this time, that is out of scope for a component, better suited to an integration or frontend module.