import requests

weather_api = 'a0b60fdadbff75ee2e48ebb59ab78815'  # апи с openweathermap для получения погоды


def get_weather(city="Москва"):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data = res.json()
        weather = data['list'][0]
        # city_id = data['list'][0]['id']

        response = [
            'Погода в городе {} \n\n'.format(city),
            weather['weather'][0]['description'].capitalize() + '\n',
            'Температура: {} ℃\n'.format(weather['main']['temp']),
            'Ощущается, как: {} ℃\n'.format(weather['main']['feels_like'])
        ]
        # возвращаю погоду
        return response

    except Exception as e:
        print("Exception (find):", e)
        pass


if __name__ == '__main__':
    get_weather()
