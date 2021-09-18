import pprint
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List

import aiohttp
import asyncio
import ssl

from bs4 import BeautifulSoup

base_url = 'https://vdt.the23.ru'


def get_url_list(date_from, date_to):
    url_list = list()

    delta = timedelta(days=1)
    for i in range((date_to - date_from).days):
        current_date = date_from + i*delta
        url = base_url + '/?date=' + datetime.strftime(current_date, "%Y-%m-%d")
        url_list.append(url)

    return url_list


async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.text()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


@dataclass
class Flight:
    position: int
    country: str
    player: str
    time: float
    green_delta: float
    delta: float
    drone: str
    date: datetime
    updates: int


@dataclass
class Leaderboard:
    season: int
    date: date
    map: str
    track: str
    flights: List[Flight] = None


def main():
    loop = asyncio.get_event_loop()

    date_from = date(2021, 9, 10)
    date_to = date(2021, 9, 12)
    url_list = get_url_list(date_from, date_to)

    htmls = loop.run_until_complete(fetch_all(url_list, loop))
    soup = BeautifulSoup(htmls[0], 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    rows.pop(0)  # удаление заголовка
    flights = list()
    for row in rows:
        cells = row.find_all('td')
        flight = Flight(
            position=          int(cells[1].text),
            country=               cells[2].img['title'],
            player=                cells[2].text.lstrip(),
            time=            float(cells[3].find(text=True, recursive=False)),
            green_delta=     float(cells[3].sup.text or 0.0),
            delta=           float(cells[4].text),
            drone=                 cells[5].text,
            date=datetime.strptime(cells[6].text, '%Y-%m-%d %H:%M'),
            updates=           int(cells[7].text),
        )
        flights.append(flight)
    pprint.pprint(flights)


if __name__ == '__main__':
    main()
