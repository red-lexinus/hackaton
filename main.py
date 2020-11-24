import telebot
import weather
import users

bot = telebot.TeleBot('1462012638:AAFrR38qrVfg7anRelUid5hEAtbaNtq7rH8')

global_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
global_markup.row('Интересные места', 'Обновить геолокацию')
global_markup.row('Погода', 'Курс валют')


# current_ind = -1  # индекс пользователя в массиве пользователей


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=global_markup)

    if message.from_user.id not in users.users_list.keys():  # если такого пользователя не существует
        new_user = users.User()  # создаем нового пользователя
        users.users_list[message.from_user.id] = new_user

    # print(message.from_user.id)
    # print(users.users_list)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, чем могу тебе помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'До связи!')
        # простые сообщения


    elif message.text.lower() == 'обновить геолокацию':
        print('m', message)
        location_btn = telebot.types.KeyboardButton('Разрешить использовать геолокацию', request_location=True)
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row(location_btn)
        bot.send_message(message.chat.id, 'Включите геоданные', reply_markup=markup)
        # запрос геоданных

    elif message.text.lower() == 'интересные места':
        bot.send_message(message.chat.id, 'Эта функция пока не работает:')
        # bot.send_message(message.chat.id, 'Интересные места в городе Москва:')
        # интересные места

    elif message.text.lower() == 'курс валют':
        bot.send_message(message.chat.id, 'Эта функция пока не работает:')
        # bot.send_message(message.chat.id, 'Курс валют на сегодня:')
        # курс валют

    elif message.text.lower() == 'погода':
        bot.send_message(message.chat.id, ''.join(weather.get_weather()))  # погода из файла weather.py
        # погода

    else:
        bot.send_message(message.chat.id, 'Я не знаю, что ответить')
        # ответ на неизвестные сообщения


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    # print(message)
    pass


@bot.message_handler(content_types=['location'])
def handle_loc(message):
    bot.send_message(message.chat.id, 'Мы получили вашу геолокацию', reply_markup=global_markup)
    # print(message.location)


bot.polling()
