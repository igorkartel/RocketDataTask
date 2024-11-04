import aiofiles
import asyncio
import json
import re

from aiohttp import ClientSession
from lxml import etree, html


def process_addresses(div_blocks):
    addresses = []
    for div in div_blocks:
        div_html = etree.tostring(div, pretty_print=True, encoding="unicode")
        if '<h4><strong>Dirección:</strong></h4>' in div_html:
            address = div.xpath('.//h4[strong[text()="Dirección:"]]/following-sibling::node()[1]/text()')
            if len(address) > 1:
                address = ", ".join(address).strip()
                addresses.append(address.replace("\xa0", " "))
            elif len(address) == 1:
                addresses.append(address[0].strip().replace("\xa0", " "))
        if '<p><strong>Dirección</strong>: <br/>' or '<p><strong>Dirección</strong>:<br/>' in div_html:
            address = div.xpath('.//p[strong[contains(text(), "Dirección")]]/br/following-sibling::text()[1]')
            if len(address) > 1:
                address = ", ".join(address).strip()
                addresses.append(address.replace("\xa0", " "))
            elif len(address) == 1:
                addresses.append(address[0].strip().replace("\xa0", " "))
        if '<p><span style="font-weight: 600;">Dirección</span>:<br/>' in div_html:
            address = div.xpath('.//p[span[contains(text(), "Dirección")]]/br/following-sibling::text()[1]')
            if len(address) > 1:
                address = ", ".join(address).strip()
                addresses.append(address.replace("\xa0", " "))
            elif len(address) == 1:
                addresses.append(address[0].strip().replace("\xa0", " "))
        if 'Dirección' not in div_html:
            address = None
            addresses.append(address)

    return addresses


def process_phones(div_blocks):
    phones = []
    for div in div_blocks:
        div_html = etree.tostring(div, pretty_print=True, encoding="unicode")
        if '<h4><strong>Teléfono:</strong></h4>' in div_html:
            phone = div.xpath('.//h4[strong[text()="Teléfono:"]]/following-sibling::node()[1]/text()')
            if len(phone) == 1:
                if "Contacto: " in phone[0]:
                    phone[0] = phone[0].replace("Contacto: ", "")
                phones.append(phone[0].strip())
        if '<p><strong>Teléfono</strong>: <br/>' or '<p><strong>Teléfono</strong>:<br/>' in div_html:
            phone = div.xpath('.//p[strong[contains(text(), "Teléfono")]]/br/following-sibling::text()[1]')
            if len(phone) == 1:
                if "Contacto: " in phone[0]:
                    phone[0] = phone[0].replace("Contacto: ", "")
                phones.append(phone[0].strip())
        if '<p><span style="font-weight: 600;">Teléfono</span>:<br/>' in div_html:
            phone = div.xpath('.//p[span[contains(text(), "Teléfono")]]/br/following-sibling::text()[1]')
            if len(phone) == 1:
                if "Contacto: " in phone[0]:
                    phone[0] = phone[0].replace("Contacto: ", "")
            phones.append(phone[0].strip())
        if 'Teléfono' not in div_html:
            phone = None
            phones.append(phone)

    return phones


def process_working_hours(div_blocks):
    working_hours = []
    for div in div_blocks:
        div_html = etree.tostring(div, pretty_print=True, encoding="unicode")
        if '<h4>Horario de atención:</h4>' in div_html:
            time = div.xpath('.//h4[text()="Horario de atención:"]/following-sibling::node()/text()')
            if len(time) > 1:
                time = ", ".join(time).strip()
                working_hours.append(time.replace("\xa0", " "))
            elif len(time) == 1:
                working_hours.append(time[0].strip().replace("\xa0", " "))
        if '<p><strong>Horario de atención</strong>:</p>' in div_html:
            time = div.xpath('.//p[strong[contains(text(), "Horario de atención")]]/following-sibling::p/text()')
            if len(time) > 1:
                time = ", ".join(time).strip()
                working_hours.append(time.replace("\xa0", " "))
            elif len(time) == 1:
                working_hours.append(time[0].strip().replace("\xa0", " "))
        if '<p><strong>Horario de atención</strong>: <br/>' in div_html:
            time = div.xpath('.//p[strong[contains(text(), "Horario de atención")]]/br/following-sibling::text()[1]')
            if len(time) > 1:
                time = ", ".join(time).strip()
                working_hours.append(time.replace("\xa0", " "))
            elif len(time) == 1:
                working_hours.append(time[0].strip().replace("\xa0", " "))
        if '<p><span style="font-weight: 600;">Horario de atención</span>:</p>' in div_html:
            time = div.xpath('.//p[span[contains(text(), "Horario de atención")]]/following-sibling::p/text()')
            if len(time) > 1:
                time = ", ".join(time).strip()
                working_hours.append(time.replace("\xa0", " "))
            elif len(time) == 1:
                working_hours.append(time[0].strip().replace("\xa0", " "))
        if 'Horario de atención' not in div_html:
            time = None
            working_hours.append(time)

    return working_hours


async def parse_latlon_from_google_geocode(session, places):
    latlon = []
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    api_key = "AIzaSyA78cJxZOhUOAnoNehx-TrG0xQeSgIU2Yk"
    try:
        for place in places:
            async with session.get(url=f"{base_url}?address={place}&key={api_key}") as response:
                results = await response.json()

                if results['results']:
                    location = results['results'][0]
                    latitude = float(location['geometry']['location']['lat'])
                    longitude = float(location['geometry']['location']['lng'])
                    coordinates = [latitude, longitude]
                    latlon.append(coordinates)
                else:
                    latlon.append(None)

        return latlon

    except Exception as e:
        print(f"Failed to parse data from website: {e}")
        return latlon


async def parse_santa_elena(url):
    city_locations = []
    try:
        async with (ClientSession() as session):
            async with session.get(url=url) as response:
                if response.status != 200:
                    print(f"Failed to fetch {url}: status code {response.status}")
                    return city_locations

                tree = html.fromstring(await response.text())

                name = tree.xpath('//meta[@property="og:site_name"]/@content')
                name = name[0].strip() if name else None

                city = tree.xpath(
                    '//ul[@class="sub-menu elementor-nav-menu--dropdown"]'
                    '/li[contains(@class, "menu-item menu-item-type-post_type menu-item-object-page current-menu-item page_item")]'
                    '/a/text()'
                )
                city = city[0].split(" ")[-1] if city else None

                places = tree.xpath('//div[@class="elementor-widget-container"]'
                                    '//h3[contains(@class, "elementor-heading-title elementor-size-default")]')
                places = [re.sub(r'\s+', ' ', " ".join(pl.xpath('.//text()')).strip()) for pl in places]

                div_blocks = tree.xpath(
                    '//div[@class="elementor-widget-container"][.//strong[contains(text(), "Dirección")] or .//span[contains(text(), "Dirección")]]'
                )

                addresses = process_addresses(div_blocks)
                phones = process_phones(div_blocks)
                working_hours = process_working_hours(div_blocks)

                latlon = await parse_latlon_from_google_geocode(session, places)

                for place, address, phone, hours, coord in zip(places, addresses, phones, working_hours, latlon):
                    city_locations.append(
                        {
                            "name": name,
                            "address": city + ", " + place + ", " + address,
                            "latlon": coord,
                            "phones": phone,
                            "working_hours": hours
                        }
                    )

                return city_locations

    except Exception as e:
        print(f"Failed to parse data from website: {e}")
        return city_locations


async def write_to_json_file(locations):
    try:
        async with aiofiles.open('santaelena.json', 'w', encoding="utf-8") as file:
            await file.write(json.dumps(locations, ensure_ascii=False, indent=4))

    except (OSError, IOError) as e:
        print(f"Error while writing to a file: {e}")


async def main():
    urls = [
        "https://www.santaelena.com.co/tiendas-pasteleria/tienda-medellin/",
        "https://www.santaelena.com.co/tiendas-pasteleria/tienda-bogota/",
        "https://www.santaelena.com.co/tiendas-pasteleria/tienda-monteria/",
        "https://www.santaelena.com.co/tiendas-pasteleria/tiendas-pastelerias-pereira/",
        "https://www.santaelena.com.co/tiendas-pasteleria/nuestra-pasteleria-en-barranquilla-santa-elena/",
    ]

    tasks = [asyncio.create_task(parse_santa_elena(url)) for url in urls]

    results = await asyncio.gather(*tasks)

    locations = [res for result in results for res in result]

    await write_to_json_file(locations)


if __name__ == "__main__":
    asyncio.run(main())
