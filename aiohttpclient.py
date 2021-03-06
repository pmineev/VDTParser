import asyncio
import ssl
from datetime import timedelta, datetime

import aiohttp

base_url = 'https://vdt.the23.ru'

loop = asyncio.get_event_loop()


def get_url_list(date_from, date_to):
    url_list = list()

    delta = timedelta(days=1)
    for i in range((date_to - date_from).days + 1):
        current_date = date_from + i*delta
        url = base_url + '/?date=' + datetime.strftime(current_date, "%Y-%m-%d")
        url_list.append(url)

    return url_list


async def fetch(session, url, event_poster=None):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        text = await response.text(errors='replace')

        if event_poster:
            event_poster.post()

        return text


async def fetch_all(urls, event_poster=None):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url, event_poster) for url in urls], return_exceptions=True)

        return results


def get_vdt_list(event_poster):
    return loop.run_until_complete(fetch_all([base_url], event_poster))[0]


def get_leaderboards_htmls(date_from, date_to, event_poster):
    url_list = get_url_list(date_from, date_to)

    leaderboards_htmls = loop.run_until_complete(fetch_all(url_list, event_poster))

    return list(filter(lambda html: html != '404', leaderboards_htmls))
