import requests
import re


def parse_text(text):
    pattern = r'/\w+.+'
    city = re.search(pattern, text).group()
    return city[1:]

def get_weater(city):
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

def main():
    # print(get_weater())
    print(get_weater(parse_text('/санкт-петербург')))


if __name__ == '__main__':
    main()