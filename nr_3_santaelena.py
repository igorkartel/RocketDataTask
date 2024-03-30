import json
import requests
from bs4 import BeautifulSoup
from nr_3_santaelena_coordinates import coords_medellin, coords_bogota, coords_monteria, coords_pereira, coords_barranquilla


# На сайте находим нужные нам страницы по каждому городу, которые отдают данные о магазинах
# Записываем адреса страниц в переменные, импортируем списки координат для каждого города из отдельного модуля
# Создаем отдельную функцию для обработки каждого города, т.к. страница каждого города формирует данные по-разному
# и к обработке каждой страницы нужен свой подход
# В каждой функции создаем объект BeautifulSoup и используем его для работы с каждым документом
medellin = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-medellin/"
bogota = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-bogota/"
monteria = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-monteria/"
pereira = "https://www.santaelena.com.co/tiendas-pasteleria/tiendas-pastelerias-pereira/"
barranquilla = "https://www.santaelena.com.co/tiendas-pasteleria/nuestra-pasteleria-en-barranquilla-santa-elena/"


# Функция для города Medellin
def loc_medellin(url, coord_list):
    # Объявляем пустой список для будущего добавления в него всех адресов города
    all_locations = []

    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    # Исследуем документ и находим все блоки, где лежат нужные нам данные
    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        # Объявляем пустой словарь для будущей сборки в него всех данных о магазине
        location = {}

        # Находим и извлекаем название магазина. Исключаем все значения None, добавляем в словарь
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})

        # Находим и извлекаем блок данных с инфо о магазине. Форматируем их и приводим к списку
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("\n", "---")
            if "---Local" in a:
                a = a.replace("---Local", " Local")
            a = a.split("---")
            for item in a:
                if item == "Horario de atención:":
                    a.remove(item)

            # Находим и извлекаем адрес, телефон и рабочее время, преобразуем в нужный формат
            address = "Medellín, " + a[0].replace("Dirección:", "").strip()
            phones = a[1].replace("Teléfono:", "").strip()
            working_hours = a[2:]

            # Добавляем их в словарь. Координатам присваиваем None, т.к. они будут обрабатываться далее
            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        # Сформированный словарь по магазину добавляем в список локаций города, исключая все значения None
        all_locations.append(location)
        locations = [item for item in all_locations if item]

    # Обновляем пару ключ-значение с координатами для каждого магазина
    if len(locations) == len(coord_list):
        for item, dictionary in enumerate(locations):
            dictionary["latlon"] = coord_list[item]

    return locations


# Функция для города Bogota
def loc_bogota(url, coord_list):
    # Объявляем пустой список для будущего добавления в него всех адресов города
    all_locations = []

    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    # Исследуем документ и находим все блоки, где лежат нужные нам данные
    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        # Объявляем пустой словарь для будущей сборки в него всех данных о магазине
        location = {}

        # Находим и извлекаем название магазина. Исключаем все значения None, добавляем в словарь
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip().replace("\n", " ")})

        # Находим и извлекаем блок данных с инфо о магазине. Форматируем их и приводим к списку
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().split("Horario de atención:")

            # Находим и извлекаем адрес, телефон и рабочее время, преобразуем в нужный формат
            # На странице Боготы нет телефонов, поэтому присваиваем None
            address = "Bogotá, " + a[0].replace("Dirección:", "").strip()
            phones = None
            working_hours = a[1:]
            if "m.Domingo" in working_hours[0]:
                working_hours = working_hours[0].replace("m.Domingo", "m.---Domingo").split("---")

            # Добавляем их в словарь. Координатам присваиваем None, т.к. они будут обрабатываться далее
            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        # Сформированный словарь по магазину добавляем в список локаций города, исключая все значения None
        all_locations.append(location)
        locations = [item for item in all_locations if item]

    # Обновляем пару ключ-значение с координатами для каждого магазина
    if len(locations) == len(coord_list):
        for item, dictionary in enumerate(locations):
            dictionary["latlon"] = coord_list[item]

    return locations


# Функция для города Monteria
def loc_monteria(url, coord_list):
    # Объявляем пустой список для будущего добавления в него всех адресов города
    all_locations = []

    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    # Исследуем документ и находим все блоки, где лежат нужные нам данные
    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        # Объявляем пустой словарь для будущей сборки в него всех данных о магазине
        location = {}

        # Находим и извлекаем название магазина. Исключаем все значения None, добавляем в словарь
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})

        # Находим и извлекаем блок данных с инфо о магазине. Форматируем их и приводим к списку
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("Teléfono:", "---").replace("Horario de atención:", "---").split("---")

            # Находим и извлекаем адрес, телефон и рабочее время, преобразуем в нужный формат
            address = "Montería, " + a[0].replace("Dirección:", "").replace("MonteríaLocal", "Montería Local").strip()
            phones = a[1].strip()
            working_hours = a[2:]
            working_hours = working_hours[0].replace("m.Domingos", "m.---Domingos").split("---")

            # Добавляем их в словарь. Координатам присваиваем None, т.к. они будут обрабатываться далее
            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        # Сформированный словарь по магазину добавляем в список локаций города, исключая все значения None
        all_locations.append(location)
        locations = [item for item in all_locations if item]

    # Обновляем пару ключ-значение с координатами для каждого магазина
    if len(locations) == len(coord_list):
        for item, dictionary in enumerate(locations):
            dictionary["latlon"] = coord_list[item]

    return locations


# Функция для города Pereira
def loc_pereira(url, coord_list):
    # Объявляем пустой список для будущего добавления в него всех адресов города
    all_locations = []

    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    # Исследуем документ и находим все блоки, где лежат нужные нам данные
    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        # Объявляем пустой словарь для будущей сборки в него всех данных о магазине
        location = {}

        # Находим и извлекаем название магазина. Исключаем все значения None, добавляем в словарь
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})

        # Находим и извлекаем блок данных с инфо о магазине. Форматируем их и приводим к списку
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("Teléfono:Contacto:", "---").replace("Horario de atención:", "---").split("---")

            # Находим и извлекаем адрес, телефон и рабочее время, преобразуем в нужный формат
            address = "Pereira, " + a[0].replace("Dirección:", "").strip()
            phones = a[1].strip()
            working_hours = a[2:]

            # Добавляем их в словарь. Координатам присваиваем None, т.к. они будут обрабатываться далее
            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        # Сформированный словарь по магазину добавляем в список локаций города, исключая все значения None
        all_locations.append(location)
        locations = [item for item in all_locations if item]

    # Обновляем пару ключ-значение с координатами для каждого магазина
    if len(locations) == len(coord_list):
        for item, dictionary in enumerate(locations):
            dictionary["latlon"] = coord_list[item]

    return locations


# Функция для города Barranquilla
def loc_barranquilla(url, coord_list):
    # Объявляем пустой список для будущего добавления в него всех адресов города
    all_locations = []

    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    # Исследуем документ и находим все блоки, где лежат нужные нам данные
    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        # Объявляем пустой словарь для будущей сборки в него всех данных о магазине
        location = {}

        # Находим и извлекаем название магазина. Исключаем все значения None, добавляем в словарь
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})

        # Находим и извлекаем блок данных с инфо о магазине. Форматируем их и приводим к списку
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("Teléfono:Contacto:", "---").replace("Horario de atención:", "---").split("---")

            # Находим и извлекаем адрес, телефон и рабочее время, преобразуем в нужный формат
            address = "Barranquilla, " + a[0].replace("Dirección:", "").strip()
            phones = a[1].strip()
            working_hours = a[2:]
            working_hours = working_hours[0].replace("m.Domingos", "m.---Domingos").split("---")

            # Добавляем их в словарь. Координатам присваиваем None, т.к. они будут обрабатываться далее
            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        # Сформированный словарь по магазину добавляем в список локаций города, исключая все значения None
        all_locations.append(location)
        locations = [item for item in all_locations if item]

    # Обновляем пару ключ-значение с координатами для каждого магазина
    if len(locations) == len(coord_list):
        for item, dictionary in enumerate(locations):
            dictionary["latlon"] = coord_list[item]

    return locations


# Вызываем функцию для кадого города, передавая через параметр адреса страниц и списки координат
city_1 = loc_medellin(medellin, coords_medellin)
city_2 = loc_bogota(bogota, coords_bogota)
city_3 = loc_monteria(monteria, coords_monteria)
city_4 = loc_pereira(pereira, coords_pereira)
city_5 = loc_barranquilla(barranquilla, coords_barranquilla)

# Формируем общий список всех локаций всех городов
all_cities = city_1 + city_2 + city_3 + city_4 + city_5

# Когда список сформирован, записываем все данные в json-файл
with open('santaelena.json', 'w', encoding="utf-8") as file:
    json.dump(all_cities, file, ensure_ascii=False, indent=4)