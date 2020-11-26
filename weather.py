import requests

weather_api = 'a0b60fdadbff75ee2e48ebb59ab78815'  # апи с openweathermap для получения погоды


def simple_weather(user, bot, message):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'lat': user.location.latitude, 'lon': user.location.longitude,
                                   'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data = res.json()
        weather = data['list'][0]

        res2 = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'lat': user.location.latitude, 'lon': user.location.longitude,
                                   'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data2 = res2.json()

        emojis = ''
        if weather["rain"] is not None:
            emojis += '🌧️'
        if weather["snow"] is not None:
            emojis += '❄️️'
        if weather["clouds"] is not None:
            emojis += '☁️️️'

        response = [
            f'_Погода в районе {data2["name"]}_\n\n',
            f'{weather["weather"][0]["description"].capitalize()}    {emojis}\n\n',
            f'Температура         *{weather["main"]["temp"]}* ℃\n',
            f'Ощущается как    *{weather["main"]["feels_like"]}* ℃\n'
        ]

        bot.send_message(message.chat.id, ''.join(response), parse_mode='Markdown')

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка')
        print("Exception (find):", e)


def detailed_weather(user, bot, message):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'lat': user.location.latitude, 'lon': user.location.longitude,
                                   'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data = res.json()
        weather = data['list'][0]

        res2 = requests.get("http://api.openweathermap.org/data/2.5/weather",
                            params={'lat': user.location.latitude, 'lon': user.location.longitude,
                                    'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data2 = res2.json()

        emojis = ''
        if weather["rain"] is not None:
            emojis += '🌧️'
        if weather["snow"] is not None:
            emojis += '❄️️'
        if weather["clouds"] is not None:
            emojis += '☁️️️'

        response = [
            f'_Погода в районе {data2["name"]}_\n\n',
            f'{weather["weather"][0]["description"].capitalize()}    {emojis}\n\n',
            f'Температура *{weather["main"]["temp"]}* ℃\n',
            f'(от *{weather["main"]["temp_min"]}* до *{weather["main"]["temp_max"]}* ℃)\n',
            f'Ощущается как    *{weather["main"]["feels_like"]}* ℃\n\n'
            f'Давление             *{weather["main"]["pressure"]}* гПа\n'
            f'Влажность            *{weather["main"]["humidity"]}* %\n'
            f'Скорость ветра   *{weather["wind"]["speed"]}* м/с\n'
        ]

        bot.send_message(message.chat.id, ''.join(response), parse_mode='Markdown')

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка')
        print("Exception (find):", e)


def three_days_weather(user, bot, message):
    try:
        res = requests.get("https://api.openweathermap.org/data/2.5/onecall",
                           params={'lat': user.location.latitude, 'lon': user.location.longitude,
                                   'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data = res.json()

        res2 = requests.get("http://api.openweathermap.org/data/2.5/weather",
                            params={'lat': user.location.latitude, 'lon': user.location.longitude,
                                    'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data2 = res2.json()

        start = f'_Погода в районе {data2["name"]} на 3 дня_\n\n',
        bot.send_message(message.chat.id, start, parse_mode='Markdown')

        for i in range(3):
            weather = data['daily'][i]
            emojis = ''
            if 'rain' in weather.keys():
                emojis += '🌧️'
            if 'snow' in weather.keys():
                emojis += '❄️️'
            if 'clouds' in weather.keys():
                emojis += '☁️️️'

            days = {
                0: 'Сегодня',
                1: 'Завтра',
                2: 'Послезавтра',
            }

            response = [
                f'*{days[i]}*\n',
                f'{weather["weather"][0]["description"].capitalize()}    {emojis}\n',
                f'Температура\n',
                f'Утро *{weather["temp"]["morn"]}* ℃    День *{weather["temp"]["day"]}* ℃\n',
                f'Вечер *{weather["temp"]["eve"]}* ℃    Ночь *{weather["temp"]["night"]}* ℃\n',
            ]

            bot.send_message(message.chat.id, ''.join(response), parse_mode='Markdown')

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка')
        print("Exception (find):", e)


def get_temp(user):
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'lat': user.location.latitude, 'lon': user.location.longitude,
                               'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
    data = res.json()
    weather = data['list'][0]

    return weather["main"]["feels_like"]
