import pprint
from datetime import date, datetime, timedelta

import aiohttp
import asyncio
import ssl

from parsers import parse_vdt_list, parse_flights

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
