import aiofiles
import asyncio
import json

from aiohttp import ClientSession
from bs4 import BeautifulSoup


def format_coordinates(coordinates):
    try:
        latlon = [float(item.strip()) for item in coordinates]
        return latlon

    except ValueError as e:
        print(f"Error while coordinates' formatting: {e}")
        return None


def format_working_hours(time):
    try:
        lst = []
        for t in time:
            aaa = t.find_all("div")
            lst.append(aaa)
        working_hours = lst[1][1].text.strip()
        return working_hours

    except Exception as e:
        print(f"Error while working hours' formatting: {e}")
        return None


async def parse_dentalia(url: str, locations):
    try:
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status != 200:
                    print(f"Failed to fetch {url}: status code {response.status}")
                    return locations

                soup = BeautifulSoup(await response.text(), "html.parser")
                clinics_geodata = soup.find_all('div', {"class": "dg-map_clinic-card w-dyn-item"})

                for clinic in clinics_geodata:
                    name = clinic.get("m8l-c-filter-name").strip()

                    address = clinic.get("m8l-c-filter-location").strip()

                    coordinates = clinic.get("m8l-c-list-coord").split(",")
                    latlon = format_coordinates(coordinates)

                    time = clinic.find_all('div', class_='dg-map_clinic-info_row')
                    working_hours = format_working_hours(time)

                    phones = clinic.find('a', {"m8l-name": "telefono"}).text.strip()

                    location = {
                        "name": name or None,
                        "address": address or None,
                        "latlon": latlon,
                        "phones": phones or None,
                        "working_hours": working_hours,
                    }

                    locations.append(location)

            return locations

    except Exception as e:
        print(f"Failed to parse data from website: {e}")
        return locations


async def write_to_json_file(locations):
    try:
        async with aiofiles.open('dentalia.json', 'w', encoding="utf-8") as file:
            await file.write(json.dumps(locations, ensure_ascii=False, indent=4))

    except (OSError, IOError) as e:
        print(f"Error while writing to a file: {e}")


async def main():
    locations = []
    url = "https://www.dentalia.com/clinicas"

    locations = await asyncio.create_task(parse_dentalia(url, locations))

    await write_to_json_file(locations)


if __name__ == "__main__":
    asyncio.run(main())
