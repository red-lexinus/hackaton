import json
import requests
import telebot


url = 'https://api.foursquare.com/v2/venues/explore'


def get_places(user, bot, message, q='', lim=5):
    params = dict(
        client_id='2LT5KTOBNMCSHSNDC51KL5CPYOADWAL4GKUH1GNMIA2WF23S',
        client_secret='RCOAJRQUS2XEK3FK2TIWIZVIETYKEWQQWWPFLPLAXZT45XBA',
        v='20201124',
        ll='{},{}'.format(user.location.latitude, user.location.longitude),
        query=q,
        locale='ru'
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)['response']

    text = f'В радиусе {data["suggestedRadius"]} метров от вас нашлось {data["totalResults"]} места\n\n'
    text += f'Вот *{lim}* из них:'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

    places = data['groups'][0]['items']

    for i in range(user.places_starts_at, user.places_starts_at + lim):
        place = places[i]
        try:
            text = f'*{place["venue"]["name"]}*\n'
            text += f'Находится по адресу: {place["venue"]["location"]["address"]}\n'
            text += f'В {place["venue"]["location"]["distance"]} метрах от вас\n'
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
            bot.send_location(message.chat.id, place["venue"]["location"]["lat"], place["venue"]["location"]["lng"])
        except KeyError:
            i -= 1
    user.places_starts_at += lim


if __name__ == '__main__':
    get_places({'longitude': 37.805942, 'latitude': 55.813916})
