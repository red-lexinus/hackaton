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

    params = dict(
        client_id='2LT5KTOBNMCSHSNDC51KL5CPYOADWAL4GKUH1GNMIA2WF23S',
        client_secret='RCOAJRQUS2XEK3FK2TIWIZVIETYKEWQQWWPFLPLAXZT45XBA',
        v='20201125',
        ll='{},{}'.format(user.location.latitude, user.location.longitude),
        query=query,
        locale='ru'
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)['response']

    user.places_count[choice] = data["totalResults"]

    how_many_show = lim if user.saw_counter[choice] + lim < user.places_count[choice] \
        else user.places_count[choice] - user.saw_counter[choice]

    text = f'В радиусе {data["suggestedRadius"]} метров от вас нашлось {data["totalResults"]} места\n\n'
    text += f'Вот *{how_many_show}* из них:'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

    places = data['groups'][0]['items']
    for i in range(how_many_show):
        while "address" not in places[user.saw_counter[choice]]["venue"]["location"]:
            user.saw_counter[choice] += 1
            if user.saw_counter[choice] >= user.places_count[choice] - 1:
                user.saw_counter[choice] = 0

        place = places[user.saw_counter[choice]]
        text = f'*{place["venue"]["name"]}*\n'
        text += f'Находится по адресу: {place["venue"]["location"]["address"]}\n'
        text += f'В {place["venue"]["location"]["distance"]} метрах от вас\n'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        bot.send_location(message.chat.id, place["venue"]["location"]["lat"], place["venue"]["location"]["lng"])

        user.saw_counter[choice] += 1

    if user.saw_counter[choice] >= user.places_count[choice] - 1:
        user.saw_counter[choice] = 0

    users.save_users()



