from aiohttpclient import get_vdt_list, get_leaderboards_htmls
from parsers import parse_vdt_list, parse_flights


def get_leaderboards(date_from, date_to):
    vdt_list_html = get_vdt_list()
    leaderboard_htmls = get_leaderboards_htmls(date_from, date_to)
    leaderboards = parse_vdt_list(vdt_list_html, date_from, date_to)
    for leaderboard, html in zip(leaderboards, leaderboard_htmls):
        flights, world_record = parse_flights(html)
        leaderboard.flights = flights
        leaderboard.world_record = world_record
    return leaderboards