import json
import requests
from bs4 import BeautifulSoup


# На сайте находим нужные нам страницы по каждому городу, которые отдают данные о магазинах
# Записываем адреса страниц в переменные и создаем функцию, которая их будет обрабатывать
# В функции создаем объект BeautifulSoup и используем его для работы с каждым документом
achinsk = "https://achinsk.yapdomik.ru/about"
berdsk = "https://berdsk.yapdomik.ru/about"
krasnoyarsk = "https://krsk.yapdomik.ru/about"
novosibirsk = "https://nsk.yapdomik.ru/about"
omsk = "https://omsk.yapdomik.ru/about"
tomsk = "https://tomsk.yapdomik.ru/about"

# Объявляем пустой список для будущего добавления в него всех адресов
locations = []

def yapdomik_locations(url):
    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    # Вытаскиваем название (у всех магазинов будет одно), город (для формирования адреса) и телефон
    # Приводим их в требуемый формат
    name = soup.find('div', {"class": "container--about__title"}).text.split('»')[0].replace('«', '')
    city = soup.find('a', {"class": "city-select__current link link--underline"}).text.strip()
    phones = soup.find('a', {"class": "link link--black link--underline"}).text.strip()

    # Находим нужный нам скрипт, который формирует данные о магазинах. Эти данные доступны в разметке
    # Вытаскиваем из него данные и преобразуем их в формат json, удобный для дальнейшей работы
    # Находим и извлекаем данные о магазинах
    scripts = soup.find_all('script')
    for script in scripts:
        script_content = script.string
        if script_content and "window.initialState" in script_content:
            data = script_content.replace('window.initialState = ', '')
            shops = json.loads(data)["shops"]
            break

    # Вытаскиваем и преобразуем в нужный формат адрес, координаты, рабочее время каждого магазина
    for shop in shops:
        address = city + ", " + shop["address"]

        latitude = shop["coord"]["latitude"]
        longitude = shop["coord"]["longitude"]
        coordinates = []
        coordinates.append(latitude)
        coordinates.append(longitude)

        schedule = shop["schedule"]
        # Преобразуем дни недели в нужный формат. Скриптом дни недели отдаются в виде чисел от 0 до 7.
        # Анализируем, какое число соответствует какому дню недели.
        # Объявляем список с днями недели. Индекс каждого дня недели соответствует числу, которое обозначает этот день
        weekdays = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]
        start_day = schedule[0]["startDay"]
        end_day = schedule[0]["endDay"]
        for item, value in enumerate(weekdays):
            if item == start_day:
                start_day = value
            if item == end_day:
                end_day = value
        # Преобразуем время в нужный формат
        open_time = schedule[0]["openTime"].split(":")
        open_time = ":".join(open_time[0:2])
        close_time = schedule[0]["closeTime"].split(":")
        close_time = ":".join(close_time[0:2])
        # Формируем рабочее время, склеивая все необходимые данные
        working_hours =  start_day + " - " + end_day + " " + open_time + " - " + close_time

        # Формируем словарь со всеми данными о магазине и добавляем его в список локаций
        location = {"name": name,
                    "address": address,
                    "latlon": coordinates,
                    "phones": phones,
                    "working_hours": working_hours,
                    }

        locations.append(location)

    return locations


# Вызываем функцию для кадого магазина, передавая через параметр их адреса
yapdomik_locations(achinsk)
yapdomik_locations(berdsk)
yapdomik_locations(krasnoyarsk)
yapdomik_locations(novosibirsk)
yapdomik_locations(omsk)
yapdomik_locations(tomsk)

# Когда список сформирован, записываем все данные в json-файл
with open('yapdomik.json', 'w', encoding="utf-8") as file:
    json.dump(locations, file, ensure_ascii=False, indent=4)