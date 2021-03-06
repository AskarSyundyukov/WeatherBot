#Messages
START_MESSAGE = 'Привет! Меня зовут WeatherBot и я могу рассказать тебе о погоде.' \
                'Для получения списка доступных команд, ты можешь использовать команду /help.'


HELP_MESSAGE = 'Тебе доступны следующие команды:\n'              \
               '/help - показывает данный текст\n'               \
               '/weather - получить погоду в г.{default_city}\n'


WEATHER_INFO_MESSAGE = "Сводка погоды по городу {city} \n\n"     \
                       "Состояние: {description}\n"              \
                       "Температура: {temperature} °C \n"        \
                       "Влажность: {humidity} % \n"              \
                       "Скорость ветра: {wind_speed} м/с \n\n"
