import logging
from pyowm import OWM
from pyowm.exceptions.api_response_error import NotFoundError
#Best

class WeatherInfo:
    def __init__(self, **kwargs):
        self.city = kwargs.get("city")
        self.temperature = kwargs.get("temperature")
        self.humidity = kwargs.get("humidity")
        self.wind_speed = kwargs.get("wind_speed")
        self.description = kwargs.get("description")


class WeatherReceiver:
    def __init__(self, weather_token):
        self.owm = OWM(weather_token, language='ru')

    def get_weather_by_city(self, city):
        try:
            received_weather = self.owm.weather_at_place(city).get_weather()
        except NotFoundError as exc:
            logging.warning(f"Cannot get weather for {city} city. Failed with exception: {exc}")
        else:
            return WeatherInfo(
                city=city,
                temperature=received_weather.get_temperature("celsius")["temp"],
                wind_speed=received_weather.get_wind()["speed"],
                humidity=received_weather.get_humidity(),
                description=received_weather.get_detailed_status(),
            )
