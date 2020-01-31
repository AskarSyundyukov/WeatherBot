FROM python:3.6

ARG BOT_TOKEN
ARG WEATHER_TOKEN

ENV ENV_BOT_TOKEN=$BOT_TOKEN
ENV ENV_WEATHER_TOKEN=$WEATHER_TOKEN

COPY . /weather-bot
WORKDIR "/weather-bot"

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT "/weather-bot/src/main.py" "--bot_token" $ENV_BOT_TOKEN "--weather_token" $ENV_WEATHER_TOKEN
