import telebot
from telebot import types
import weather
import users
import places
import converter

API_KEY = '1462012638:AAFrR38qrVfg7anRelUid5hEAtbaNtq7rH8'
bot = telebot.TeleBot(API_KEY)

global_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
global_markup.row('Близкие места', 'Обновить мою геолокацию')
global_markup.row('Погода', 'Курс валют')


def get_geo(message):
    location_btn = telebot.types.KeyboardButton('Разрешить использовать геолокацию', request_location=True)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(location_btn)
    bot.send_message(message.chat.id, 'Включите геоданные', reply_markup=markup)


def check_user(message):
    if message.from_user.id not in users.users_list.keys():  # если такого пользователя не существует
        new_user = users.User()  # создаем нового пользователя
        users.users_list[message.from_user.id] = new_user


@bot.message_handler(commands=['start'])
def start_message(message):
    check_user(message)
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=global_markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    check_user(message)
    cid = message.chat.id
    uid = message.from_user.id
    user = users.users_list[uid]

    if message.text.lower() == 'привет':
        bot.send_message(cid, 'Привет, чем могу тебе помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(cid, 'До связи!')
        # простые сообщения

    elif message.text.lower() == 'обновить мою геолокацию':
        get_geo(message)
        # запрос геоданных

    elif message.text.lower() == 'близкие места':
        if user.location == {}:  # если локация ещё не записана
            bot.send_message(cid, 'Повторите попытку после включения геоданных')
            get_geo(message)
        else:
            count = 3
            places.get_places(user, bot, message, '', count)
        # интересные места

    elif message.text.lower() == 'курс валют':
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("доллар", callback_data='0')
        item5 = types.InlineKeyboardButton("резервная валюта мира", callback_data='2')
        item2 = types.InlineKeyboardButton("евро", callback_data='1')
        item3 = types.InlineKeyboardButton("английский фунт", callback_data='3')
        item4 = types.InlineKeyboardButton("швейцарский франк", callback_data='4')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        bot.send_message(message.chat.id, 'Какая Валюта нужна?', reply_markup=markup)
        bot.send_message(cid,
                         'Полная информация находится на сайте https://www.banki.ru/products/currency/cash/moskva/#bank-rates')

    elif message.text.lower() == 'погода':
        if user.location == {}:  # если локация ещё не записана
            bot.send_message(cid, 'Повторите попытку после включения геоданных')
            get_geo(message)
        else:
            weather.get_weather(user, bot, message)
        # погода

    else:
        bot.send_message(cid, 'Я не знаю, что ответить')
        # ответ на неизвестные сообщения


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    # print(message)
    pass


@bot.message_handler(content_types=['location'])
def handle_loc(message):
    check_user(message)
    cid = message.chat.id
    uid = message.from_user.id
    user = users.users_list[uid]

    bot.send_message(message.chat.id, 'Мы получили вашу геолокацию', reply_markup=global_markup)
    user.location = message.location
    user.is_have_location = True
    # print(users.users_list[message.from_user.id].location)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            arr_valua = ['доллар', 'евро', 'резервная валюта мира', 'английский фунт', 'швейцарский франк']
            bot.send_message(call.message.chat.id, 'официальный курс валюты {} на сегодня: {}'.format(arr_valua[int(call.data)],
                                                                                           converter.converter_1(
                                                                                               int(call.data))))
    except:
        pass


bot.polling()
