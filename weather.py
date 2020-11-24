import requests

weather_api = 'a0b60fdadbff75ee2e48ebb59ab78815'  # апи с openweathermap для получения погоды


def get_weather(user, bot, message, city="Москва"):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data = res.json()
        weather = data['list'][0]

        emojis = ''
        if weather["rain"] is not None:
            emojis += '🌧️'
        if weather["snow"] is not None:
            emojis += '❄️️'
        if weather["clouds"] is not None:
            emojis += '☁️️️'

        response = [
            f'_Погода в городе {city}_\n\n',
            f'{weather["weather"][0]["description"].capitalize()} {emojis}\n',
            f'Температура         *{weather["main"]["temp"]}* ℃\n',
            f'Ощущается как    *{weather["main"]["feels_like"]}* ℃\n'
        ]

        bot.send_message(message.chat.id, ''.join(response), parse_mode='Markdown')

    except Exception as e:
        print("Exception (find):", e)
        bot.send_message(message.chat.id, 'Ошибка')
        pass


if __name__ == '__main__':
    get_weather()
