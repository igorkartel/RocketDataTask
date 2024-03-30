import json
import requests
from bs4 import BeautifulSoup
import threading
import time


medellin = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-medellin/"
bogota = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-bogota/"
monteria = "https://www.santaelena.com.co/tiendas-pasteleria/tienda-monteria/"
pereira = "https://www.santaelena.com.co/tiendas-pasteleria/tiendas-pastelerias-pereira/"
barranquilla = "https://www.santaelena.com.co/tiendas-pasteleria/nuestra-pasteleria-en-barranquilla-santa-elena/"

all_locations = []

def loc_medellin(medellin):

    data = requests.get(medellin)

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


def loc_in_threads():
    thread_1 = threading.Thread(target=loc_medellin, args=(medellin,), name="medellin")
    thread_2 = threading.Thread(target=loc_bogota, args=(bogota,), name="bogota")
    thread_3 = threading.Thread(target=loc_monteria, args=(monteria,), name="monteria")
    thread_4 = threading.Thread(target=loc_pereira, args=(pereira,), name="pereira")
    thread_5 = threading.Thread(target=loc_barranquilla, args=(barranquilla,), name="barranquilla")
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    thread_5.start()
    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()
    thread_5.join()


start_threads = time.time()
loc_in_threads()
end_threads = time.time()
# print(f'Потоки выполнились за {end_threads - start_threads:.4f} с.')


d = requests.get("https://www.google.com/maps/d/viewer?&mid=1PjEJHvVyruJdbvV9JxP1czJJfVtWjko&ll=6.241232300000023%2C-75.58764529999999&z=10")

soup = BeautifulSoup(d.text, "html.parser")
print(soup)
