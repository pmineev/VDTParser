import pprint
from datetime import date

import asyncio

from aiohttpclient import base_url, get_url_list, fetch_all
from parsers import parse_vdt_list, parse_flights


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
