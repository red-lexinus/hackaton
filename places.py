import json
import requests
import users


url = 'https://api.foursquare.com/v2/venues/explore'


def get_places(user, bot, message, choice=0, lim=5):
    query = ''
    if choice == 1:
        query = 'ресторан'  # и кафе
    elif choice == 2:
        query = 'музей'
    elif choice == 3:
        query = 'парк'
    elif choice == 4:
        query = 'кино'
    elif choice == 5:
        query = 'магазин'
    # выбор места для запроса

    params = dict(
        client_id='2LT5KTOBNMCSHSNDC51KL5CPYOADWAL4GKUH1GNMIA2WF23S',
        client_secret='RCOAJRQUS2XEK3FK2TIWIZVIETYKEWQQWWPFLPLAXZT45XBA',
        v='20201125',
        ll='{},{}'.format(user.location.latitude, user.location.longitude),
        query=query,
        locale='ru'
    )
    req = requests.get(url=url, params=params)
    data = json.loads(req.text)['response']
    # запрос к апи

    user.places_count[choice] = data["totalResults"]
    # всего мест

    if data["totalResults"] == 0:
        bot.send_message(message.chat.id, 'Мест не найдено')
        return 0

    how_many_show = lim if user.saw_counter[choice] + lim < user.places_count[choice] \
        else user.places_count[choice] - user.saw_counter[choice]
    # сколько мест показывать (чтобы не выходить за массив)

    text = f'В радиусе {data["suggestedRadius"]} метров от вас нашлось {data["totalResults"]} места\n\n'
    text += f'Вот *{how_many_show}* из них:'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    # вывод информации

    places = data['groups'][0]['items']
    # все места

    for i in range(how_many_show):
        while "address" not in places[user.saw_counter[choice]]["venue"]["location"]:  # выводить места только с адресом
            user.saw_counter[choice] += 1
            if user.saw_counter[choice] >= user.places_count[choice] - 1:
                user.saw_counter[choice] = 0

        place = places[user.saw_counter[choice]]  # текущее место

        # text = f'*{place["venue"]["name"]}*\n'
        # text += f'Находится по адресу: {place["venue"]["location"]["address"]}\n'
        # text += f'В {place["venue"]["location"]["distance"]} метрах от вас\n'
        # bot.send_message(message.chat.id, text, parse_mode='Markdown')
        # старый вариант вывода

        bot.send_venue(message.chat.id, place["venue"]["location"]["lat"], place["venue"]["location"]["lng"],
                       disable_notification=True, title=place["venue"]["name"],
                       address=place["venue"]["location"]["address"])
        # новый вариант вывода (можно вернуть старый)

        user.saw_counter[choice] += 1

    if user.saw_counter[choice] >= user.places_count[choice] - 1:
        user.saw_counter[choice] = 0
    # проверка, чтобы сбрасывать счетчик, когда места заканчиваются

    users.save_users()
    return 1


def get_all_places(user):
    all_queries = ['', 'ресторан', 'музей', 'парк', 'кино', 'магазин']  # '' - все места

    for query in all_queries:
        params = dict(
            client_id='2LT5KTOBNMCSHSNDC51KL5CPYOADWAL4GKUH1GNMIA2WF23S',
            client_secret='RCOAJRQUS2XEK3FK2TIWIZVIETYKEWQQWWPFLPLAXZT45XBA',
            v='20201125',
            ll='{},{}'.format(user.location.latitude, user.location.longitude),
            query=query,
            locale='ru',
            limit=15
        )

        req = requests.get(url=url, params=params)
        data = json.loads(req.text)['response']

        places = data['groups'][0]['items']

        if query == '':
            user.all_places = places
        if query == 'ресторан':
            user.food = places
        if query == 'музей':
            user.museums = places
        if query == 'парк':
            user.parks = places
        if query == 'кино':
            user.cinemas = places
        if query == 'магазин':
            user.shops = places

        users.save_users()

