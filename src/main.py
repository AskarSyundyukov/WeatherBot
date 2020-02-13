#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import messages
from weather.WeatherReceiver import WeatherReceiver
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
DEFAULT_CITY = 'Санкт-Петербург'


def handle_start_command(update, context):
    logging.info(f"/start command received from "
                 f"{update.effective_user.full_name} ({update.effective_chat.id})")
    update.message.reply_text(messages.START_MESSAGE)


def handle_help_command(update, context):
    logging.info(f"/help command received from "
                 f"{update.effective_user.full_name} ({update.effective_chat.id})")
    update.message.reply_text(messages.HELP_MESSAGE.format(
        default_city=DEFAULT_CITY,
    ))


def handle_weather_command(update, context):
    logging.info(f"/weather command received from "
                 f"{update.effective_user.full_name} ({update.effective_chat.id})")
    weather_info = weather_receiver.get_weather_by_city(DEFAULT_CITY)  # TODO check for None
    update.message.reply_text(messages.WEATHER_INFO_MESSAGE.format(
        city=DEFAULT_CITY,
        temperature=weather_info.temperature,
        humidity=weather_info.humidity,
        wind_speed=weather_info.wind_speed,
        description=weather_info.description,
    ))


def handle_text_message(update, context):
    logging.info(f"Text message received from "
                 f"{update.effective_user.full_name} "
                 f"({update.effective_chat.id}): "
                 f"{update.message.text}")


def handle_error(update, context):
    logging.warning(f"Update {update} caused error {context.error}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Weather bot')
    parser.add_argument('--bot_token', type=str, help='Telegram token', required=True)
    parser.add_argument('--weather_token', type=str, help='Weather API token', required=True)
    parser.add_argument('--debug', default=False, help='Enable debug', required=False)
    args = parser.parse_args()

    if args.debug:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO

    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    logging.info(f"WeatherBot started...")

    weather_receiver = WeatherReceiver(args.weather_token)

    updater = Updater(args.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_start_command))
    dispatcher.add_handler(CommandHandler('help', handle_help_command))
    dispatcher.add_handler(CommandHandler('weather', handle_weather_command))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_text_message),)
    dispatcher.add_error_handler(handle_error)

    updater.start_polling()
    updater.idle()
