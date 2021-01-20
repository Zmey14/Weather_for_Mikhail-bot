from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
# from flask_talisman import Talisman
import requests
import json
import re


# __name__ ссылка на текущий файл
app = Flask(__name__)
sslify = SSLify(app)

# app = Flask(__name__)
# Talisman(app)

URL = 'https://api.telegram.org/bot1412485068:AAF91ZLpganAuMl0QtPbNOf4RdSlEI_WjlU/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# send_message имеет 2 обязательных параметра- chat_id, text
def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+.+'
    city = re.search(pattern, text).group()
    return city[1:]


def get_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},RU&units=metric&APPID=05d7dbad41cb773b1e9b1629e3ba6b5f'.format(city)
    r = requests.get(url).json()
    name_city = r['name']
    weather_main = r['weather'][0]['main']
    temp = r['main']['temp']
    temp_feels_like = r['main']['feels_like']
    temp_feels_min = r['main']['temp_min']
    temp_feels_max = r['main']['temp_max']
    wind = r['wind']['speed']
    weather = f'Город: {name_city}\nСостояние погоды: {weather_main}\nТемпература: {temp}C\nОщущается: {temp_feels_like}C\nМинимум: {temp_feels_min}C\nМаксимум: {temp_feels_max}C\nВетер: {wind} м/c'
    return weather


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.methods == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+.+'

        if re.search(pattern, message):
            city = get_weather(parse_text(message))
            send_message(chat_id, text=city)

        # write_json(r)

        return jsonify(r)
    return '<h1>Hello! Im bot.</h1>'


# Вызов метода run
if __name__ == '__main__':
    app.run()
