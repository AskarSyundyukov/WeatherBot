import telebot
import config
import random
import pyowm
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рандомное число")
    item2 = types.KeyboardButton("Какая погода сейчас?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)

        elif message.text == 'Какая погода сейчас?':
            city = bot.send_message(message.chat.id, "В каком городе вывести погоду?")
            bot.register_next_step_handler(city, weather)

        else:
            bot.send_message(message.chat.id, 'Error')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как дела?",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))


def weather(message):
    try:
        owm = pyowm.OWM(config.TOKEN_WEATHER)
        city = message.text
        weather = owm.weather_at_place(city)
        w = weather.get_weather()
        temperature = w.get_temperature("celsius")["temp"]
        wind = w.get_wind()["speed"]
        hum = w.get_humidity()
        desc = w.get_detailed_status()
        bot.send_message(message.chat.id, "Сейчас в городе " + str(city) + " \n" + str(desc) + ", \nТемпература: " + str(
            temperature) + "°C, \nВлажность: " + str(hum) + "%, \nСкорость ветра: " + str(wind) + "м/с.")


    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.send_message(message.chat.id, 'Город не найден!')


bot.polling(none_stop=True)
