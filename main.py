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
global_markup.row('Пройти Опрос')
arr_answer = {'опрос_00': 4, 'опрос_01': 4, 'опрос_02': 4, 'опрос_03': 4, 'опрос_04': 4, }
secreat_txt = ''
def get_geo(message):
    location_btn = telebot.types.KeyboardButton('Разрешить использовать геолокацию', request_location=True)
    cancel_btn = telebot.types.KeyboardButton('Отмена')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(location_btn, cancel_btn)
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
    global secreat_txt, arr_answer
    check_user(message)
    cid = message.chat.id
    uid = message.from_user.id
    user = users.users_list[uid]

    if message.text.lower() == 'привет':
        bot.send_message(cid, 'Привет, чем могу тебе помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(cid, 'До связи!')
    elif message.text.lower() == 'отмена':
        bot.send_message(cid, 'Чем ещё я могу помочь?', reply_markup=global_markup)
        # простые сообщения

    elif message.text.lower() == 'обновить мою геолокацию':
        get_geo(message)
        # запрос геоданных

    elif message.text.lower() == 'близкие места':
        if user.location == {}:  # если локация ещё не записана
            bot.send_message(cid, 'Повторите попытку после включения геоданных')
            get_geo(message)
        else:
            # count = 3
            # places.get_places(user, bot, message, '', count)
            # интересные места

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Все места поблизости", callback_data='0'))
            markup.add(types.InlineKeyboardButton("Рестораны", callback_data='1'))
            markup.add(types.InlineKeyboardButton("Кафе", callback_data='2'))
            markup.add(types.InlineKeyboardButton("Музеи", callback_data='3'))
            markup.add(types.InlineKeyboardButton("Парки", callback_data='4'))
            markup.add(types.InlineKeyboardButton("Магазины", callback_data='5'))

            bot.send_message(cid, 'Какие места найти?', reply_markup=markup)


    elif message.text.lower() == 'курс валют':
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Доллар 💲", callback_data='0')
        item5 = types.InlineKeyboardButton("Резервная валюта мира", callback_data='2')
        item2 = types.InlineKeyboardButton("Евро 🇪🇺", callback_data='1')
        item3 = types.InlineKeyboardButton("Английский фунт 💷", callback_data='3')
        item4 = types.InlineKeyboardButton("Швейцарский франк 🇨🇭", callback_data='4')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)

        bot.send_message(cid, 'Какая Валюта нужна?', reply_markup=markup)
        bot.send_message(cid,
                         'Полная информация находится на сайте https://www.banki.ru/products/currency/cash/moskva/#bank-rates')

    elif message.text.lower() == 'погода':
        if user.location == {}:  # если локация ещё не записана
            bot.send_message(cid, 'Повторите попытку после включения геоданных')
            get_geo(message)
        else:
            weather.get_weather(user, bot, message)
        # погода
    elif message.text.lower() == 'пройти опрос':
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Да", callback_data='опрос_000')
        item5 = types.InlineKeyboardButton("Иногда)", callback_data='опрос_001')
        item2 = types.InlineKeyboardButton("почти никогда", callback_data='опрос_002')
        item3 = types.InlineKeyboardButton("Совершенно нет", callback_data='опрос_003')
        markup.add(item1, item3)
        markup.add(item5, item2)
        bot.send_message(message.chat.id, 'Вам нравится без особого повода ходить по магазинам?', reply_markup=markup)


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

    bot.send_message(cid, 'Мы получили вашу геолокацию', reply_markup=global_markup)
    user.location = message.location
    user.is_have_location = True
    # print(users.users_list[message.from_user.id].location)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global secreat_txt, arr_answer
    cid = call.message.chat.id
    uid = call.from_user.id
    user = users.users_list[uid]
    try:
        if call.message.text == 'Какая Валюта нужна?':
            # if call.data[:-2] == 'currency'
            arr_valua = ['доллар', 'евро', 'резервная валюта мира', 'английский фунт', 'швейцарский франк']
            bot.send_message(cid, 'Курс валюты {} на сегодня\n*{:.2f}* рублей'.format(arr_valua[int(call.data[-1])],
                                                                                      converter.converter_1(
                                                                                          int(call.data[-1]))),
                             parse_mode='Markdown')
        elif call.message.text == 'Какие места найти?':
            query = ''
            if int(call.data) == 1:
                query = 'ресторан'
            elif int(call.data) == 2:
                query = 'кафе'
            elif int(call.data) == 3:
                query = 'музей'
            elif int(call.data) == 4:
                query = 'парк'
            elif int(call.data) == 5:
                query = 'магазин'

            places.get_places(user, bot, call.message, query, 3)
        elif 'опрос_00' == call.data[:-1]:
            num = int(call.data[-2:])
            arr_answer[call.data[0:-1]] = num
            secreat_txt = call.data[0:-1]
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Да", callback_data='опрос_010')
            item5 = types.InlineKeyboardButton("Иногда хочется", callback_data='опрос_011')
            item2 = types.InlineKeyboardButton("почти никода", callback_data='опрос_012')
            item3 = types.InlineKeyboardButton("Совершенно нет", callback_data='опрос_013')
            markup.add(item1, item3)
            markup.add(item5, item2)
            bot.send_message(cid,
                             'Скажите вам нравится спонтанно посещать театры и кино?', reply_markup=markup)

        elif 'опрос_01' == call.data[:-1]:
            num = int(call.data[-2:])
            arr_answer[call.data[0:-1]] = num
            secreat_txt = call.data[0:-1]
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Да", callback_data='опрос_020')
            item5 = types.InlineKeyboardButton("Иногда)", callback_data='опрос_021')
            item2 = types.InlineKeyboardButton("почти никогда", callback_data='опрос_022')
            item3 = types.InlineKeyboardButton("Совершенно нет", callback_data='опрос_023')
            markup.add(item1, item3)
            markup.add(item5, item2)
            bot.send_message(cid,
                             'Хотите ли вы гулять в парках?', reply_markup=markup)
        elif 'опрос_02' == call.data[:-1]:
            num = int(call.data[-2:])
            arr_answer[call.data[0:-1]] = num
            secreat_txt = call.data[0:-1]

            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Да", callback_data='опрос_030')
            item5 = types.InlineKeyboardButton("Иногда хочу)", callback_data='опрос_031')
            item2 = types.InlineKeyboardButton("почти всегда не хочется", callback_data='опрос_032')
            item3 = types.InlineKeyboardButton("Совершенно нет", callback_data='опрос_033')
            markup.add(item1, item3)
            markup.add(item5, item2)
            bot.send_message(cid,
                             'хотите ли вы для разнообразия посмотреть на гостиницы'
                             ' и снова начать завидовать кому-нибудь?',
                             reply_markup=markup)
        elif 'опрос_03' == call.data[:-1]:
            num = int(call.data[-2:])
            arr_answer[call.data[0:-1]] = num
            secreat_txt = call.data[0:-1]

            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Да", callback_data='опрос_040')
            item5 = types.InlineKeyboardButton("Иногда)", callback_data='опрос_041')
            item2 = types.InlineKeyboardButton("почти никогда", callback_data='опрос_042')
            item3 = types.InlineKeyboardButton("Совершенно нет", callback_data='опрос_043')
            markup.add(item1, item3)
            markup.add(item5, item2)
            bot.send_message(cid,
                             'ходите ли вы в неизвестные вам рестораны?', reply_markup=markup)

        elif 'опрос_04' == call.data[:-1]:
            num = int(call.data[-2:])
            arr_answer[call.data[0:-1]] = num
            secreat_txt = call.data[0:-1]

            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("-5", callback_data='опрос_050')
            item5 = types.InlineKeyboardButton("-10", callback_data='опрос_051')
            item2 = types.InlineKeyboardButton("-15", callback_data='опрос_052')
            item3 = types.InlineKeyboardButton("-20", callback_data='опрос_053')
            item6 = types.InlineKeyboardButton("-25", callback_data='опрос_054')
            item7 = types.InlineKeyboardButton("-30", callback_data='опрос_055')
            markup.add(item1, item5)
            markup.add(item2, item3)
            markup.add(item6, item7)
            bot.send_message(cid,
                             'При какой темпиратуре вы не хотите выходить на прогулку?', reply_markup=markup)
        elif 'опрос_05' == call.data[:-1]:
            num = int(call.data[-2:])
            arr_answer[call.data[0:-1]] = num
            secreat_txt = call.data[0:-1]
            bot.send_message(cid,
                             'Спасибо за пройденный тест, возможно на данный момент наш бот не'
                             ' способен искать места по вашим интересам, но скоро это точно изменится)')




    except:
        pass


bot.polling()
