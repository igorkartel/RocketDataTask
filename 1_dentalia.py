import json
import requests
from bs4 import BeautifulSoup

# На сайте находим нужную нам страницу, которая отдает данные о клиниках
# Через DevTools находим нужный нам файл с данными о клиниках, которые формируются динамически
# Извлекаем его, создаем объект BeautifulSoup и используем его для работы с документом
data = requests.post("https://dentalia.com/clinica/?nocache=1711652476",
                     data={
                         "action": "jet_engine_ajax",
                         "handler": "get_listing",
                         "page_settings[post_id]": "5883",
                         "page_settings[queried_id]": "344706|WP_Post",
                         "page_settings[element_id]": "c1b6043",
                         "page_settings[page]": "1",
                         "listing_type": "elementor",
                         "isEditMode": "false"
                     })

html_content = data.json()["data"]["html"]

soup = BeautifulSoup(html_content, "html.parser")

# Объявляем пустой список для будущего добавления в него всех адресов
locations = []

# Исследуем документ и находим все блоки, где лежат нужные нам данные
clinics = soup.find_all('div', {"class": "elementor elementor-330"})

# В каждом найденном блоке находим нужные нам данные, приводим их в требуемый формат
for clinic in clinics:
    # Находим и извлекаем название клиники
    name = clinic.find('h3', {"class": "elementor-heading-title elementor-size-default"}).text.strip()

    # Находим блок, где лежат данные об адресе, телефоне, рабочем времени и координатах
    contact_info = clinic.find_all('div', {"class": "jet-listing-dynamic-field__content"})

    # Находим и извлекаем адрес, преобразуем в нужный формат
    address = contact_info[0].text.strip()

    # Находим и извлекаем номер телефона, преобразуем в нужный формат
    phones = contact_info[1].text
    phones = phones.replace("Teléfono(s):", "").strip().split("\r\n")
    phones = [item.strip() for item in phones]

    # Находим и извлекаем рабочее время, преобразуем в нужный формат
    working_hours = contact_info[2].text
    working_hours = working_hours.replace("Horario:", "").strip().split("\r\n")
    working_hours = [item.strip() for item in working_hours]

    # Находим и извлекаем координаты, преобразуем в нужный формат
    gps_link = clinic.find('a', {"class": "elementor-button-link elementor-button elementor-size-md"})["href"]
    if "@" in gps_link:
        coordinates = gps_link.split('@')[1].split('/')[0].split(",")[0:2]
        coordinates = [float(item) for item in coordinates]
    else:
        coordinates = None

    # Формируем словарь со всеми данными о клинике и добавляем его в список локаций
    location = {"name": name,
                "address": address,
                "latlon": coordinates,
                "phones": phones,
                "working_hours": working_hours,
                }

    locations.append(location)

# Когда список сформирован, записываем все данные в json-файл
with open('dentalia.json', 'w', encoding="utf-8") as file:
    json.dump(locations, file, ensure_ascii=False, indent=4)