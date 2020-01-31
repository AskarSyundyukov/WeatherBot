DEFAULT_CITY = 'Санкт-Петербург'

START_MESSAGE = 'Привет! Меня зовут WeatherBot и я могу рассказать тебе о погоде.' \
                'Для получения списка доступных команд, ты можешь использовать команду /help.'


HELP_MESSAGE = f'Тебе доступны следующие команды:\n'              \
               f'/help - показывает данный текст\n'               \
               f'/weather - получить погоду в г.{DEFAULT_CITY}\n'


WEATHER_INFO_MESSAGE = "Сводка погоды по городу {city} \n\n"     \
                       "Состояние: {description}\n"       \
                       "Температура: {temperature} °C \n"   \
                       "Влажность: {humidity} % \n"       \
                       "Скорость ветра: {wind_speed} м/с \n\n"
