import json
import requests
from bs4 import BeautifulSoup


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

locations = []

clinics = soup.find_all('div', {"class": "elementor elementor-330"})

for clinic in clinics:
    name = clinic.find('h3', {"class": "elementor-heading-title elementor-size-default"}).text.strip()

    contact_info = clinic.find_all('div', {"class": "jet-listing-dynamic-field__content"})
    address = contact_info[0].text.strip()

    phones = contact_info[1].text
    phones = phones.replace("Teléfono(s):", "").strip().split("\r\n")
    phones = [item.strip() for item in phones]

    working_hours = contact_info[2].text
    working_hours = working_hours.replace("Horario:", "").strip().split("\r\n")
    working_hours = [item.strip() for item in working_hours]

    gps_link = clinic.find('a', {"class": "elementor-button-link elementor-button elementor-size-md"})["href"]
    if "@" in gps_link:
        coordinates = gps_link.split('@')[1].split('/')[0].split(",")[0:2]
        coordinates = [float(item) for item in coordinates]
    else:
        coordinates = None

    location = {"name": name,
                "address": address,
                "latlon": coordinates,
                "phones": phones,
                "working_hours": working_hours,
                }

    locations.append(location)


with open('dentalia.json', 'w', encoding="utf-8") as file:
    json.dump(locations, file, ensure_ascii=False, indent=4)