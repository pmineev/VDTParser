import pprint
from datetime import date

from aiohttpclient import get_vdt_list, get_leaderboards
from parsers import parse_vdt_list, parse_flights


def main():
    date_from = date(2021, 9, 10)
    date_to = date(2021, 9, 12)

    vdt_list_html = get_vdt_list()
    leaderboard_htmls = get_leaderboards(date_from, date_to)

    leaderboards = parse_vdt_list(vdt_list_html, date_from, date_to)

    for leaderboard, html in zip(leaderboards, leaderboard_htmls):
        flights, world_record = parse_flights(html)
        leaderboard.flights = flights
        leaderboard.world_record = world_record

    pprint.pp(leaderboards)


if __name__ == '__main__':
    main()
