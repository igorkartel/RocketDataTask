import json
import requests
from bs4 import BeautifulSoup


medellin = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-medellin/"
bogota = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-bogota/"
monteria = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-monteria/"
pereira = "https://www.santaelena.com.co/tiendas-pasteleria/tiendas-pastelerias-pereira/"
barranquilla = "https://www.santaelena.com.co/tiendas-pasteleria/nuestra-pasteleria-en-barranquilla-santa-elena/"



def loc_medellin(url):
    all_locations = []
    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        location = {}
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("\n", "---")
            if "---Local" in a:
                a = a.replace("---Local", " Local")
            a = a.split("---")
            for item in a:
                if item == "Horario de atención:":
                    a.remove(item)

            address = "Medellín, " + a[0].replace("Dirección:", "").strip()
            phones = a[1].replace("Teléfono:", "").strip()
            working_hours = a[2:]

            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        all_locations.append(location)
        locations = [item for item in all_locations if item]

    return locations


def loc_bogota(url):
    all_locations = []
    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        location = {}
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip().replace("\n", " ")})
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().split("Horario de atención:")
            address = "Bogotá, " + a[0].replace("Dirección:", "").strip()
            phones = None
            working_hours = a[1:]
            if "m.Domingo" in working_hours[0]:
                working_hours = working_hours[0].replace("m.Domingo", "m.---Domingo").split("---")

            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        all_locations.append(location)
        locations = [item for item in all_locations if item]

    return locations


def loc_monteria(url):
    all_locations = []
    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        location = {}
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("Teléfono:", "---").replace("Horario de atención:", "---").split("---")
            address = "Montería, " + a[0].replace("Dirección:", "").replace("MonteríaLocal", "Montería Local").strip()
            phones = a[1].strip()
            working_hours = a[2:]
            working_hours = working_hours[0].replace("m.Domingos", "m.---Domingos").split("---")

            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        all_locations.append(location)
        locations = [item for item in all_locations if item]

    return locations


def loc_pereira(url):
    all_locations = []
    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        location = {}
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("Teléfono:Contacto:", "---").replace("Horario de atención:", "---").split("---")

            address = "Pereira, " + a[0].replace("Dirección:", "").strip()
            phones = a[1].strip()
            working_hours = a[2:]
            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        all_locations.append(location)
        locations = [item for item in all_locations if item]

    return locations


def loc_barranquilla(url):
    all_locations = []
    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    shops = soup.find_all('div', {"class": "elementor-column-wrap elementor-element-populated"})

    for shop in shops:
        location = {}
        name = shop.find('h3', {"class": "elementor-heading-title elementor-size-default"})
        if name is not None:
            location.update({"name": "Pasteleria Santa Elena " + name.text.strip()})
        place_info = shop.find('div', {"class": "elementor-text-editor elementor-clearfix"})
        if place_info is not None and "Dirección:" in place_info.text:
            a = place_info.text.strip().replace("Teléfono:Contacto:", "---").replace("Horario de atención:", "---").split("---")

            address = "Barranquilla, " + a[0].replace("Dirección:", "").strip()
            phones = a[1].strip()
            working_hours = a[2:]
            working_hours = working_hours[0].replace("m.Domingos", "m.---Domingos").split("---")

            location.update({"address": address,
                            "latlon": None,
                            "phones": phones,
                            "working_hours": working_hours,
                            })

        all_locations.append(location)
        locations = [item for item in all_locations if item]

    return locations

city_1 = loc_medellin(medellin)
city_2 = loc_bogota(bogota)
city_3 = loc_monteria(monteria)
city_4 = loc_pereira(pereira)
city_5 = loc_barranquilla(barranquilla)

all_cities = city_1 + city_2 + city_3 + city_4 + city_5

with open('santaelena.json', 'w', encoding="utf-8") as file:
    json.dump(all_cities, file, ensure_ascii=False, indent=4)


# d = requests.post("https://play.google.com/log?format=json&hasfast=true&authuser=0",
#                   data={
#                         "format": "json",
#                         "hasfast": "true",
#                         "authuser": "0"
#                   })
# a = d.text
# print(a)
