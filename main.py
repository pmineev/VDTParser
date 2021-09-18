import pprint
from datetime import date, datetime, timedelta

import aiohttp
import asyncio
import ssl

from bs4 import BeautifulSoup

from entities import Flight, Leaderboard

base_url = 'https://vdt.the23.ru'


def get_url_list(date_from, date_to):
    url_list = list()

    delta = timedelta(days=1)
    for i in range((date_to - date_from).days + 1):
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


def parse_vdt_list(html, date_from, date_to):
    soup = BeautifulSoup(html, 'html.parser')

    delta = timedelta(days=1)
    leaderboards = list()
    for i in range((date_to - date_from).days + 1):
        current_date = date_from + i * delta
        current_tag = soup.find(text=datetime.strftime(current_date, "%Y-%m-%d")).parent.parent
        cells = current_tag.find_all('td')
        leaderboard = Leaderboard(
            season=int(cells[0].text),
            date=current_date,
            map=cells[2].text.split('/')[0].rstrip(),
            track=cells[2].text.split('/')[1].lstrip()
        )
        leaderboards.append(leaderboard)

    return leaderboards


def parse_flights(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    rows.pop(0)  # удаление заголовка
    flights = list()
    for row in rows:
        flight = parse_flight(row)
        flights.append(flight)

    return flights


def parse_flight(row):
    cells = row.find_all('td')
    flight = Flight(
        position=int(cells[1].text),
        country=cells[2].img['title'],
        player=cells[2].text.lstrip(),
        time=float(cells[3].find(text=True, recursive=False)),
        green_delta=float(cells[3].sup.text or 0.0),
        delta=float(cells[4].text),
        drone=cells[5].text,
        date=datetime.strptime(cells[6].text, '%Y-%m-%d %H:%M'),
        updates=int(cells[7].text),
    )

    return flight


def main():
    loop = asyncio.get_event_loop()

    date_from = date(2021, 9, 10)
    date_to = date(2021, 9, 12)
    url_list = get_url_list(date_from, date_to)

    vdt_list_html = loop.run_until_complete(fetch_all([base_url], loop))[0]
    leaderboard_htmls = loop.run_until_complete(fetch_all(url_list, loop))

    leaderboards = parse_vdt_list(vdt_list_html, date_from, date_to)

    for leaderboard, html in zip(leaderboards, leaderboard_htmls):
        flights = parse_flights(html)
        leaderboard.flights = flights

    pprint.pp(leaderboards)


if __name__ == '__main__':
    main()
