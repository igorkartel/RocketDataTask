import json
import requests
from bs4 import BeautifulSoup
import threading
import time


achinsk = "https://achinsk.yapdomik.ru/about"
berdsk = "https://berdsk.yapdomik.ru/about"
krasnoyarsk = "https://krsk.yapdomik.ru/about"
novosibirsk = "https://nsk.yapdomik.ru/about"
omsk = "https://omsk.yapdomik.ru/about"
tomsk = "https://tomsk.yapdomik.ru/about"

locations = []

def yapdomik_locations(url):
    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    # Вытаскиваем имя (у всех магазинов будет одно), город (для формирования адреса) и телефон
    name = soup.find('div', {"class": "container--about__title"}).text.split('»')[0].replace('«', '')
    city = soup.find('a', {"class": "city-select__current link link--underline"}).text.strip()
    phones = soup.find('a', {"class": "link link--black link--underline"}).text.strip()

    # Вытаскиваем данные о магазинах, которые скрипт рендерит на карту
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
        # Преобразуем дни недели в нужный формат
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

        location = {"name": name,
                    "address": address,
                    "latlon": coordinates,
                    "phones": phones,
                    "working_hours": working_hours,
                    }

        locations.append(location)

    return locations


def loc_in_threads():
    thread_1 = threading.Thread(target=yapdomik_locations, args=(achinsk,), name="achinsk")
    thread_2 = threading.Thread(target=yapdomik_locations, args=(berdsk,), name="berdsk")
    thread_3 = threading.Thread(target=yapdomik_locations, args=(krasnoyarsk,), name="krasnoyarsk")
    thread_4 = threading.Thread(target=yapdomik_locations, args=(novosibirsk,), name="novosibirsk")
    thread_5 = threading.Thread(target=yapdomik_locations, args=(omsk,), name="omsk")
    thread_6 = threading.Thread(target=yapdomik_locations, args=(tomsk,), name="tomsk")
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    thread_5.start()
    thread_6.start()
    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()
    thread_5.join()
    thread_6.join()


start_threads = time.time()
loc_in_threads()
end_threads = time.time()
print(f'Потоки выполнились за {end_threads - start_threads:.4f} с.')


with open('yapdomik.json', 'w', encoding="utf-8") as file:
    json.dump(locations, file, ensure_ascii=False, indent=4)