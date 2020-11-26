import json
import requests
import users

url = 'https://api.foursquare.com/v2/venues/explore'


def get_places(user, bot, message, choice=0, lim=5, pos=0):
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

    user.places_count[choice] = data["totalResults"]

    if data["totalResults"] == 0:
        bot.send_message(message.chat.id, 'Мест не найдено')
        return 0
    elif data['totalResults'] < pos + lim:
        bot.send_message(message.chat.id, 'Мест не найдено')
        return 0
    places = data['groups'][0]['items']
    places = sort_arr(places)
    text = f'В радиусе {places[-1]["distance"]} метров от вас нашлось {data["totalResults"]} места\n\n'
    text += f'Вот *{lim}* из них:'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    for i in range(lim):
        place = places[i + pos]
        text = f'*{place["venue"]["name"]}*\n'
        text += f'Находится по адресу: {place["venue"]["location"]["address"]}\n'
        text += f'В {place["venue"]["location"]["distance"]} метрах от вас\n'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        bot.send_location(message.chat.id, place["venue"]["location"]["lat"], place["venue"]["location"]["lng"])


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
            limit=100
        )

        req = requests.get(url=url, params=params)
        data = json.loads(req.text)['response']
        places = data['groups'][0]['items']
        places = sort_arr(places)

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




def sort_arr(arr):
    for d in range(len(arr)):
        arr[d].update({'distance': arr[d]['venue']['location']['distance']})
    return sorted(arr, key=lambda x: x['distance'], reverse=False)
