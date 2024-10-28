from pprint import pprint

import aiofiles
import asyncio
import io
import json
import requests

from aiohttp import ClientSession
from lxml import etree, html


def format_working_hours(schedule):
    try:
        weekdays = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]

        start_day = schedule[0]["startDay"]
        end_day = schedule[0]["endDay"]

        for item, value in enumerate(weekdays):
            if item == start_day:
                start_day = value
            if item == end_day:
                end_day = value

        open_time = schedule[0]["openTime"].split(":")
        open_time = ":".join(open_time[0:2])
        close_time = schedule[0]["closeTime"].split(":")
        close_time = ":".join(close_time[0:2])

        working_hours = start_day + "-" + end_day + " " + open_time + "-" + close_time

        return working_hours

    except Exception as e:
        print(f"Error while working hours' formatting: {e}")
        return None


async def parse_yapdomik(url, city_locations=[]):
    try:
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status != 200:
                    print(f"Failed to fetch {url}: status code {response.status}")
                    return city_locations

                html_file = io.BytesIO(await response.read())
                htmlparser = etree.HTMLParser()
                tree = etree.parse(html_file, htmlparser)

                name = tree.xpath('//header//a[@class="site-logo"]/img/@alt')[0].strip()

                script_content = tree.xpath('//script[contains(text(),"window.initialState")]/text()')
                data = script_content[0].replace('window.initialState = ', '')

                city = json.loads(data)["city"]["name"].strip()
                phones = json.loads(data)["city"]["callCenterPhoneParameters"]["number"].strip()

                shops = json.loads(data)["shops"]
                for shop in shops:
                    # убираем лишние символы ZWSP
                    address = city + ", " + shop["address"].strip().replace("\u200B", "") + ", " + shop["geoPoint"].strip()

                    latlon = [
                        float(shop["coord"]["latitude"].strip()),
                        float(shop["coord"]["longitude"].strip())
                    ]

                    schedule = shop["schedule"]
                    working_hours = format_working_hours(schedule)

                    location = {"name": name or None,
                                "address": address or None,
                                "latlon": latlon or None,
                                "phones": phones or None,
                                "working_hours": working_hours,
                                }

                    city_locations.append(location)

                return city_locations

    except Exception as e:
        print(f"Failed to parse data from website: {e}")
        return city_locations


async def parse_name_and_city_for_berdsk(session, url="https://berdsk.yapdomik.ru/berdsk/landing/rest"):
    try:
        async with session.get(url=url) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}: status code {response.status}")
                return None, None

            html_file = io.BytesIO(await response.read())
            htmlparser = etree.HTMLParser()
            tree = etree.parse(html_file, htmlparser)

            name = tree.xpath('//meta[@itemprop="name"]/@content')
            name = name[0].strip() if name else None

            city = tree.xpath('//span[@class="g-button-select__value"]/text()')
            city = city[0].strip() if city else None

            return name, city

    except Exception as e:
        print(f"Failed to parse data from website: {e}")
        return None, None


async def parse_yapdomik_berdsk(url, city_locations = []):
    try:
        async with ClientSession() as session:
            name, city = await parse_name_and_city_for_berdsk(session)

            async with session.get(url=url) as response:
                if response.status != 200:
                    print(f"Failed to fetch {url}: status code {response.status}")
                    return None, None

                berdsk_data = requests.get(url)
                berdsk_locations = berdsk_data.json()["departments"]

                for loc in berdsk_locations:
                    address = city + ", " + loc["address"].strip()

                    latlon = [
                        float(loc["latitude"]),
                        float(loc["longitude"])
                    ]

                    phones = loc["contacts"]["phone"]

                    working_hours = loc["work_time"]

                    location = {"name": name,
                                "address": address or None,
                                "latlon": latlon or None,
                                "phones": phones or None,
                                "working_hours": working_hours or None,
                                }

                    city_locations.append(location)

                return city_locations

    except Exception as e:
        print(f"Failed to parse data from website: {e}")
        return city_locations


async def write_to_json_file(locations):
    try:
        async with aiofiles.open('yapdomik.json', 'w', encoding="utf-8") as file:
            await file.write(json.dumps(locations, ensure_ascii=False, indent=4))

    except (OSError, IOError) as e:
        print(f"Error while writing to a file: {e}")


async def main():
    urls = [
        "https://achinsk.yapdomik.ru/about",
        "https://berdsk.yapdomik.ru/api/cities/departments?city_id=1",
        "https://krsk.yapdomik.ru/about",
        "https://nsk.yapdomik.ru/about",
        "https://omsk.yapdomik.ru/about",
        "https://tomsk.yapdomik.ru/about",
    ]
    locations = []

    tasks = [
        asyncio.create_task(parse_yapdomik_berdsk(url)) if "berdsk" in url
        else asyncio.create_task(parse_yapdomik(url))
        for url in urls
    ]

    results = await asyncio.gather(*tasks)

    locations.extend(results[1])
    locations.extend(results[-1])

    await write_to_json_file(locations)

if __name__ == "__main__":
    asyncio.run(main())
